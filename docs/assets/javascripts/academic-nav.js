(function () {
  const projectLinks = [
    ["All projects", "/projects/"],
    ["AKT TRUST-LLM", "/projects/akt-trust-llm/"],
    ["KTP Connexin", "/projects/ktp-connexin/"],
    ["iCASE QinetiQ", "/projects/icase-qinetiq/"],
    ["iCASE QinetiQ via Newcastle", "/projects/icase-qinetiq-newcastle/"],
    ["Digital Twin Offshore Wind", "/projects/digital-twin-offshore-wind/"],
    ["Transforming Urban Health", "/projects/transforming-urban-health/"],
    ["Vital Knowledge Exchange", "/projects/vital-knowledge-exchange/"],
    ["Alan Turing Enrichment Award", "/projects/alan-turing-enrichment/"]
  ];

  const navLinks = [
    ["Home", "/"],
    ["Research", "/research/"],
    ["Funding", "/funding/"],
    ["Projects", "/projects/", projectLinks],
    ["Publications", "/publications/"],
    ["Supervision", "/supervision/"],
    ["Teaching", "/teaching/"],
    ["Service", "/service/"],
    ["Talks", "/talks/"],
    ["Contact", "/contact/"]
  ];

  function currentPath() {
    let path = window.location.pathname;
    if (!path.endsWith("/")) {
      path += "/";
    }
    return path;
  }

  function isActive(href) {
    const path = currentPath();
    if (href === "/") {
      return path === "/";
    }
    return path === href || path.startsWith(href);
  }

  function createLink(label, href, className) {
    const anchor = document.createElement("a");
    anchor.className = className;
    anchor.href = href;
    anchor.textContent = label;
    if (isActive(href)) {
      anchor.classList.add(className + "--active");
      anchor.setAttribute("aria-current", "page");
    }
    return anchor;
  }

  function updateActiveState(nav) {
    nav.querySelectorAll("a[href]").forEach(function (anchor) {
      const href = new URL(anchor.href).pathname;
      const active = isActive(href);
      anchor.classList.toggle("academic-topnav__link--active", active && anchor.classList.contains("academic-topnav__link"));
      anchor.classList.toggle("academic-topnav__dropdown-link--active", active && anchor.classList.contains("academic-topnav__dropdown-link"));
      if (active) {
        anchor.setAttribute("aria-current", "page");
      } else {
        anchor.removeAttribute("aria-current");
      }
    });
  }

  function mountTopNav() {
    const existing = document.querySelector("[data-academic-topnav]");
    if (existing) {
      document.documentElement.classList.add("academic-topnav-ready");
      updateActiveState(existing);
      return;
    }

    const header = document.querySelector(".md-header");
    if (!header || !header.parentElement) {
      return;
    }

    const nav = document.createElement("nav");
    nav.className = "academic-topnav";
    nav.setAttribute("data-academic-topnav", "true");
    nav.setAttribute("aria-label", "Primary navigation");

    const inner = document.createElement("div");
    inner.className = "academic-topnav__inner";

    const list = document.createElement("ul");
    list.className = "academic-topnav__list";

    navLinks.forEach(function (item) {
      const label = item[0];
      const href = item[1];
      const children = item[2];
      const li = document.createElement("li");
      li.className = "academic-topnav__item";

      const link = createLink(label, href, "academic-topnav__link");
      li.appendChild(link);

      if (children) {
        li.classList.add("academic-topnav__item--has-menu");
        link.classList.add("academic-topnav__link--menu");

        const submenu = document.createElement("ul");
        submenu.className = "academic-topnav__dropdown";
        submenu.setAttribute("aria-label", "Project pages");

        children.forEach(function (child) {
          const childLi = document.createElement("li");
          childLi.className = "academic-topnav__dropdown-item";
          childLi.appendChild(createLink(child[0], child[1], "academic-topnav__dropdown-link"));
          submenu.appendChild(childLi);
        });

        li.appendChild(submenu);
      }

      list.appendChild(li);
    });

    inner.appendChild(list);
    nav.appendChild(inner);
    updateActiveState(nav);
    header.insertAdjacentElement("afterend", nav);
    document.documentElement.classList.add("academic-topnav-ready");
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(mountTopNav);
  }

  document.addEventListener("DOMContentLoaded", mountTopNav);
})();
