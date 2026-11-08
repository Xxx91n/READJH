# EgressAPIKEY

**Multi-port socks5/http proxy gateway between AI gateways and upstream providers — sticky exit-IP routing for AI API keys, with a topology canvas.**

## Runbook

Run the tests before opening a pull request.

Upload reports to S3 after the audit.

Open config.json to set the proxy port.

## Limitations

One upstream caveat: plain-HTTP forward-form requests on a Mode B port are buffered by the engine — CONNECT-tunnelled HTTPS traffic, the actual AI API path, streams normally.

## License

See [LICENSE](LICENSE) for details.
