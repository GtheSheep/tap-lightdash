# tap-lightdash

`tap-lightdash` is a Singer tap for [Lightdash](https://www.lightdash.com/)

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
pipx install git+https://github.com/gthesheep/tap-lightdash.git
```

## Configuration

### Accepted Config Options

For authentication either `personal_access_token` or a `username/ password` combination is required.

* `url` - The URL for your Lightdash or Lightdash Cloud deployment
* `username` - Login username (email address)
* `password` - Login password
* `personal_access_token` - Personal access token for authentication

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-lightdash --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-lightdash` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-lightdash --version
tap-lightdash --help
tap-lightdash --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_lightdash/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-lightdash` CLI interface directly using `poetry run`:

```bash
poetry run tap-lightdash --help
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
cd tap-lightdash
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-lightdash --version
# OR run a test `elt` pipeline:
meltano elt tap-lightdash target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
