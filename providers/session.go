package providers

import (
	"fmt"
)

type SessionClaims struct {
	Email    string
	Verified *bool
}

type ProviderData struct {
	EmailClaim        string
	AllowUnverifiedEmail bool
}

const OIDCEmailClaim = "email"

// buildSessionFromClaims constructs a session from OIDC token claims.
// BUG: if the IDP omits email_verified entirely, claims.Verified is nil
// and the check below is skipped — unverified emails are trusted.
func (p *ProviderData) buildSessionFromClaims(claims SessionClaims) (*SessionClaims, error) {
	// `email_verified` must be present and explicitly set to `false` to be
	// considered unverified.
	verifyEmail := (p.EmailClaim == OIDCEmailClaim) && !p.AllowUnverifiedEmail
	if verifyEmail && claims.Verified != nil && !*claims.Verified {
		return nil, fmt.Errorf("email in id_token (%s) isn't verified", claims.Email)
	}

	return &claims, nil
}
