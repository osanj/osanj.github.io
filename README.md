# osanj.github.io

* development in `source` branch
* serving from `master` branch

This blog uses the `mmark` tag. For a successful build, use [hugo v0.53](https://github.com/gohugoio/hugo/releases/tag/v0.53).

To build the blog do:
1. checkout `source`
2. generate website with into `public` folder with `hugo -d public`
3. checkout `master`
4. replace all contents with the files from `public`
5. do a commit

Not beautiful, but I don't want to do another [submodule setup](https://gohugo.io/hosting-and-deployment/hosting-on-github/#github-user-or-organization-pages).
