Here is the same document in Markdown format, so you can copy, edit, store in Git, or use in documentation.

⸻


# Keycloak → NetBox Group Mapping Guide (Using Protocol Mappers)

## Purpose
This document explains how to configure **Keycloak** so that user groups and roles are included in the **OpenID Connect token**.  
NetBox (or any application) can then read those values and map them to internal groups.

---

# Authentication Flow

User → Keycloak Login
↓
Keycloak Issues Token
↓
Token contains roles/groups
↓
NetBox authentication pipeline reads token
↓
User assigned to NetBox groups

Keycloak **does not automatically include all roles or groups in tokens**.  
You must expose them using **Protocol Mappers**.

---

# Token Fields Used

Keycloak can expose authorization information in three common locations:

### 1. Realm Roles

realm_access.roles

Example:
```json
"realm_access": {
  "roles": ["superadmin"]
}

These are global roles within the Keycloak realm.

⸻

2. Client Roles

resource_access.<client>.roles

Example:

"resource_access": {
  "netbox": {
    "roles": ["staff"]
  }
}

These are roles specific to a client application (like NetBox).

⸻

3. Groups

groups

Example:

"groups": [
  "noc",
  "network-team"
]

These come from Keycloak group memberships.

⸻

Example Full Token

{
 "preferred_username": "rabi",

 "realm_access": {
   "roles": ["superadmin"]
 },

 "resource_access": {
   "netbox": {
     "roles": ["staff"]
   }
 },

 "groups": [
   "noc",
   "network-team"
 ]
}

NetBox pipeline can extract roles from all three sections.

⸻

Step 1 — Open Keycloak Admin Console
	1.	Login to Keycloak Admin Console
	2.	Select your Realm
	3.	Navigate to:

Clients → netbox

	4.	Open the Client Scopes / Mappers section

⸻

Step 2 — Add Realm Roles Mapper

Create a new mapper:

Setting	Value
Mapper Type	User Realm Role
Name	realm-roles
Token Claim Name	realm_access.roles
Add to ID Token	ON
Add to Access Token	ON
Multivalued	ON
Claim JSON Type	String

This exposes realm roles in the token.

⸻

Step 3 — Add Client Roles Mapper

Create mapper:

Setting	Value
Mapper Type	User Client Role
Client ID	netbox
Token Claim Name	resource_access.netbox.roles
Add to ID Token	ON
Add to Access Token	ON
Multivalued	ON

This exposes client roles in the token.

⸻

Step 4 — Add Groups Mapper

Create mapper:

Setting	Value
Mapper Type	Group Membership
Name	groups
Token Claim Name	groups
Add to ID Token	ON
Add to Access Token	ON
Full Group Path	OFF
Multivalued	ON

Recommended:

Full group path = OFF

Otherwise you get:

/network/noc

instead of

noc


⸻

Example NetBox Role Mapping

Keycloak Role	NetBox Group
superadmin	superadmin
staff	staff
noc	noc
network-team	network-team

Your NetBox pipeline will:

Token roles → NetBox groups


⸻

Verification

After configuring mappers:
	1.	Login through Keycloak
	2.	Capture the Access Token
	3.	Decode it using:

https://jwt.io

Confirm token contains:

realm_access.roles
resource_access.netbox.roles
groups


⸻

Troubleshooting

Roles not appearing in token

Check:
	•	Mapper Add to Access Token = ON
	•	Client scope attached to client
	•	Logout and login again

⸻

Groups showing full path

Example:

/network/noc

Fix:

Disable

Full group path

in the group mapper.

⸻

NetBox not assigning permissions

Check:
	•	Group names match exactly
	•	Pipeline reads correct claims
	•	User logs out and logs in again

⸻

Best Practice (Recommended)

Use NetBox-prefixed roles in Keycloak:

netbox:admin
netbox:viewer
netbox:noc

This prevents unrelated roles from creating NetBox groups.

Example mapping:

Keycloak Role	NetBox Group
netbox:admin	admin
netbox:noc	noc


⸻

Summary

Keycloak sends roles/groups in the token using protocol mappers.

NetBox pipeline then:

Extract roles
      ↓
Create groups if needed
      ↓
Assign groups to user
      ↓
Set staff/superuser flags

This provides centralized RBAC using Keycloak.


















