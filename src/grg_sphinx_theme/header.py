from sphinx.application import Sphinx


# Helper functions.
def generate_url(link: dict, context) -> str:
  """Generate a url to specific file if it is an internal file."""
  if "external" in link and link["external"]:
    return link["url"]
  return context["pathto"](link["url"])

def external_link_classes(link: dict) -> str:
  """Required class declaration for external links."""
  if "external" in link and link["external"]:
    return "nav-external"
  return ""

def generate_basic_link(link: dict, context) -> str:
  """Generate html code for a simple link with a tag and href populated."""
  return f"""
      <li class="nav-item">
        <a class="nav-link {external_link_classes(link)}" href="{generate_url(link, context)}">
          {link["name"]}
        </a>
      </li>"""

def generate_sub_links(links: list, context) -> str:
  """Generate html code for navigation links based upon list provided."""
  links_html = []
  for link in links:
    links_html.append(generate_basic_link(link, context))
  return "\n".join(links_html)

def generate_section_title(section: str) -> str:
  """Generate html code for navigation section title."""
  return f"""
    <li class="nav-item">
      <p class="nav-section-title nav-link">
        {section}
      </p>
    </li>"""

def generate_section_wise_links(links: list, context) -> str:
  """Generate html code for section wise navigation lists."""
  links_html = []
  for link in links:
    links_html.append(generate_section_title(link["name"]))
    links_html.append(generate_sub_links(link["children"], context))
  return "\n".join(links_html)


# Functions for registration in __init__.
def add_navbar_functions(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
  """
  Add functions so Jinja template can create navbar details.
  """
  def generate_navbar_links() -> str:
    """
    Generate different links for navbar_links configuration.
    """

    links = context.get("theme_navbar_links")

    html_links = []

    for link in links:
      # If "url" is present: direct link
      if "url" in link:
        html_links.append(generate_basic_link(link, context))

      # If "children" is present: simple dropdown
      elif "children" in link:
        html_links.append(
          f"""
          <li class="nav-item dropdown">
                <button class="btn dropdown-toggle nav-item" type="button" data-bs-toggle="dropdown" aria-expanded="false" aria-controls="pst-header-nav-more-links">
                    {link["name"]}
                </button>
                <ul id="pst-header-nav-more-links" class="dropdown-menu">
                    {generate_sub_links(link["children"], context)}
                </ul>
            </li>
          """
        )

      # If "sections" is present: section wise dropdown
      elif "sections" in link:
        html_links.append(
          f"""
          <li class="nav-item dropdown">
                <button class="btn dropdown-toggle nav-item" type="button" data-bs-toggle="dropdown" aria-expanded="false" aria-controls="pst-header-nav-more-links">
                    {link["name"]}
                </button>
                <ul id="pst-header-nav-more-links" class="dropdown-menu">
                    {generate_section_wise_links(link["sections"], context)}
                </ul>
            </li>
          """
        )


    out = "\n".join(html_links)

    return out

  # Registering functions for context to access while building
  context["generate_navbar_links"] = generate_navbar_links

