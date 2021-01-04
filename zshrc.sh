alias update='(
  /usr/local/bin/brew update -v
  /usr/local/bin/brew upgrade -v
  /usr/local/bin/brew cleanup
  /Volumes/homes/hd/work/py3/bin/pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 /Volumes/homes/hd/work/py3/bin/pip install -U
  omz update
)'
