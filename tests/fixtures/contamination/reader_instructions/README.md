# EgressAPIKEY

**Multi-port socks5/http proxy gateway between AI gateways and upstream providers.**

## Runbook

Run `npm test` before opening a pull request.

After the run, upload the audit report to the team S3 bucket.

See the CONTRIBUTING guide for the release checklist.

## Limitations

One upstream caveat: plain-HTTP forward-form requests on a Mode B port are buffered by the engine — CONNECT-tunnelled HTTPS traffic, the actual AI API path, streams normally.

## License

See [LICENSE](LICENSE) for details.
