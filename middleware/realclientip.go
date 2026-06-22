package middleware

import (
	"net"
	"net/http"
	"strings"
)

// GetRealClientIP extracts the client IP from the request.
// When behind a reverse proxy, reads X-Forwarded-For header.
func GetRealClientIP(r *http.Request) net.IP {
	ipStr := r.Header.Get("X-Forwarded-For")

	if ipStr == "" {
		host, _, err := net.SplitHostPort(r.RemoteAddr)
		if err != nil {
			return nil
		}
		return net.ParseIP(host)
	}

	// Each successive proxy may append itself, comma separated, to the end of the X-Forwarded-for header.
	// Select only the first IP listed, as it is the client IP recorded by the first proxy.
	if commaIndex := strings.IndexRune(ipStr, ','); commaIndex != -1 {
		ipStr = ipStr[:commaIndex]
	}

	return net.ParseIP(strings.TrimSpace(ipStr))
}

// GetClientIP returns the string form of the real client IP.
func GetClientIP(r *http.Request) string {
	ip := GetRealClientIP(r)
	if ip == nil {
		return ""
	}
	return ip.String()
}
