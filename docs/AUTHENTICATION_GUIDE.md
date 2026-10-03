# Authentication guide

Authentication and production authorization are not implemented in the prototype.
Streamlit session state and navigation visibility are not security controls.

## Recommended approach

Select a managed identity provider after deciding supported login methods and deployment
constraints. Prefer hosted OAuth/OIDC flows or a maintained auth integration over
hand-rolled password storage. Validate issuer, audience, signature, expiry, nonce, state,
and redirect URI. Require verified identity before account-sensitive actions.

## Implementation checklist

1. Define stable provider subject IDs and account-linking rules; email alone is not a
   stable identity key.
2. Establish server-side authenticated request context; do not accept a client-supplied
   user or role.
3. Protect session cookies with secure, HTTP-only, same-site settings where applicable;
   use CSRF protections for state-changing flows.
4. Enforce authorization at each service/API/data operation and scope queries by owner
   or organization.
5. Define admin roles, least privilege, MFA expectations, account recovery, and audit
   logging.
6. Implement logout, revocation, data export/deletion, consent, and retention workflows.
7. Test expired/revoked sessions, forged claims, account linking, privilege escalation,
   and cross-tenant access.

## Streamlit-specific note

Use Streamlit's supported identity capabilities only after checking the installed
version and host configuration. For API/worker boundaries or billing, pass a verified
server-side identity context; never treat a browser-visible session value as authority.
