# pydantic-docs

Common infrastructure to build documentation for the Pydantic projects.

## Markdown extension

`pydantic-docs` provides a [Markdown extension](https://python-markdown.github.io/extensions/), that can be used
within `mkdocs-material`:

```yaml
# mkdocs.yml
markdown_extensions:
  - pydantic_docs.mdext
```

### Blocks

The Markdown extension provides various [custom blocks](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/).

#### Public traces

The `public-trace` block can be used to embed an [iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)
for a [Logfire public trace](https://logfire.pydantic.dev/docs/guides/web-ui/public-traces/):

```md
Here is an example Logfire trace:

/// public-trace | http://logfire-us.pydantic.dev/public-trace/{uuid}
    title: 'Title for the public trace'
    caption: 'prepend'
///
```

Available options:

- `title`: The title to set in the caption. Default: no title.
- `caption`: Whether or where to display the caption:
    - `'off'`: Don't show the caption (this includes the external link to the public trace).
    - `'prepend'`: Show the caption *before* the iframe.
    - `'append'`: Show the caption *after* the iframe (the default).
- `loading`: The [`loading`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe#loading)
  iframe attribute (default: `lazy`).
