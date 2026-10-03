-- PostgreSQL starting schema. Apply through versioned migrations in production.
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    role TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('member', 'admin')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    feed_url TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    quality_score NUMERIC(4,3) CHECK (quality_score BETWEEN 0 AND 1),
    last_fetched_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    summary TEXT,
    topic TEXT NOT NULL,
    sentiment TEXT CHECK (sentiment IN ('positive', 'neutral', 'negative')),
    velocity_score NUMERIC(5,2) CHECK (velocity_score BETWEEN 0 AND 100),
    impact_score NUMERIC(5,2) CHECK (impact_score BETWEEN 0 AND 100),
    confidence_score NUMERIC(5,2) CHECK (confidence_score BETWEEN 0 AND 100),
    embedding vector(1536),
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE signal_sources (
    signal_id UUID NOT NULL REFERENCES signals(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES sources(id),
    source_url TEXT NOT NULL,
    published_at TIMESTAMPTZ,
    PRIMARY KEY (signal_id, source_id)
);

CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES app_users(id) ON DELETE CASCADE,
    topics TEXT[] NOT NULL DEFAULT '{}',
    keywords TEXT[] NOT NULL DEFAULT '{}',
    digest_frequency TEXT NOT NULL DEFAULT 'off'
        CHECK (digest_frequency IN ('off', 'daily', 'weekly')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE saved_signals (
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    signal_id UUID NOT NULL REFERENCES signals(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, signal_id)
);

CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL,
    title TEXT NOT NULL,
    body_markdown TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    stripe_customer_id TEXT UNIQUE,
    stripe_subscription_id TEXT UNIQUE,
    plan TEXT NOT NULL CHECK (plan IN ('free', 'pro', 'alpha')),
    status TEXT NOT NULL,
    current_period_end TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX signals_topic_published_idx ON signals (topic, published_at DESC);
CREATE INDEX signals_impact_idx ON signals (impact_score DESC);
CREATE INDEX reports_user_created_idx ON reports (user_id, created_at DESC);
