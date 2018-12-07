# hr-plrx-github-analysis
GitHub Analysis demo for Plrx


## Implemented features

### Packages
#### `webrequest`
Simple HTTP wrapper provides GET method, JSON-dict convertion, HTTP Headers reading.

#### `githubapi`
GitHub API wrapper allow to request repository data as objects.
Supports pagination.

#### `repoanalyzer`
VCS Repository analysis tool provides following reports:

- **Active contributors**
  Top contributors with their number of commit
- **Opened and closed pull requests**
  Number of opened and closed pull requests between dates
- **Old pull requests**
  Number of old pull requests (not closed within N days)
- **Opened and closed issues**
  Number of opened and closed issues between dates
- **Old issues**
  Number of old issues (not closed within N days)
  
### Output types
Reports can be printed as tables:

```bash
Active contributors
-------------------
Login   Commit number
maxtepkeev      493
andreiavram     11
```
or as JSON-like format:
```json
[
  {
    "name": "Active contributors",
    "headers": [
      "Login",
      "Commit number"
    ],
    "results": [
      {
        "Login": "maxtepkeev",
        "Commit number": 493
      },
...
```

## Usage
### Requirements

`analyzerepo` needs Python 3.7 and can be run with supported Windows or Linux.

### Run

First, clone this repo:

```bash
$ git clone https://github.com/dm-logv/hr-plrx-github-analysis
$ cd hr-plrx-github-analysis
$ chmod +x analyzerepo 
```

Next, you have two ways.

#### Docker

You can run `analyzerepo` as _Dockerized CLI application_. You need no Python in OS, just Docker.

```bash
$ docker build -t analyzerepo . && \
> docker run analyzerepo https://github.com/maxtepkeev/python-redmine
```

#### OS

If you have installed Python 3.7 you can run `analyzerepo` right now.

```bash
$ python analyzerepo https://github.com/maxtepkeev/python-redmine
```
or
```bash
$ ./analyzerepo https://github.com/maxtepkeev/python-redmine
```

### Command-line arguments

> You can get full list of command-line arguments: `analyzerepo -h`

### Examples

Run repo analysis with date bounds:
```bash
$ ./analyzerepo -s 2017-01-01 -e 2017-01-31 https://github.com/flutter/flutter
```

Use BasicAuth (see below):
```bash
$ docker run analyzerepo -u dm-logv -p MyPassw https://github.com/maxtepkeev/python-redmine
```

Forward proxy to Docker and get results as JSON:
```bash
$ docker run --env https_proxy=user:passW0rd@proxy.com:3128 \
>     analyzerepo --type json https://github.com/dm-logv/aero-stat
```

## Limitations

- GitHub API limits the number of requests for non-authorized users. 
  You can you the `--user` and `--password` arguments for basic authorization 
  with your account data.  
- GitHub API strictly recommends getting the next URLs for paginated responses 
  from headers instead of the URL building. 
  It makes `analyzerepo` slooow on big repositories with a high number 
  of pull requests or issues. Be patient, please.
