# tap-clientsuccess

`tap-clientsuccess` is a Singer tap for ClientSuccess.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
pipx install tap-clientsuccess
```

## Configuration

### Accepted Config Options

```bash
tap-clientsuccess --about
```

### Executing the Tap Directly

```bash
tap-clientsuccess --version
tap-clientsuccess --help
tap-clientsuccess --config CONFIG --discover > ./catalog.json
```

### Create and Run Tests

Create tests within the `tap_clientsuccess/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-clientsuccess` CLI interface directly using `poetry run`:

```bash
poetry run tap-clientsuccess --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-clientsuccess
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-clientsuccess --version
# OR run a test `elt` pipeline:
meltano elt tap-clientsuccess target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
