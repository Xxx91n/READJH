# Clean Fixture Repository (Derived from EgressAPIKEY)

A multi-port proxy gateway for AI workflows.

[![License](https://img.shields.io/github/license/Xxx91n/EgressAPIKEY)](https://github.com/Xxx91n/EgressAPIKEY/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Xxx91n/EgressAPIKEY/ci.yml)](https://github.com/Xxx91n/EgressAPIKEY/actions/workflows/ci.yml)

## Architecture

Request flow between AI gateway and upstream providers:

```bash
# Start the local gateway
python -m gateway.run --port 8080
```

See [docs/architecture.md](docs/architecture.md) for details.
Check the diagram at ![Architecture](assets/architecture.png).

## Limitations

Currently only loopback interfaces are supported in Mode A. Multi-node clustering is out of scope for the current release.

## License

See [LICENSE](LICENSE) for details.
