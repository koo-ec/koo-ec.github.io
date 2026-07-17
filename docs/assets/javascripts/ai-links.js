(function () {
  const siteUrl = "https://koo-ec.github.io/";
  const llmsUrl = "https://koo-ec.github.io/llms.txt";
  const scholarUrl = "https://scholar.google.com/citations?user=YBa4Tl8AAAAJ&hl=en";
  const openAlexUrl = "https://openalex.org/authors/A5008347336";
  const orcidUrl = "https://orcid.org/0000-0001-9318-8177";
  const prompt = [
    "Help me learn more about Dr Koorosh Aslansefat.",
    "Use these sources as context:",
    "Personal academic website: " + siteUrl,
    "LLM-readable site guide: " + llmsUrl,
    "Google Scholar: " + scholarUrl,
    "OpenAlex: " + openAlexUrl,
    "ORCID: " + orcidUrl,
    "",
    "Focus on his research in AI safety, trustworthy AI, explainable AI, SafeML, SafeLLM, SMILE/XWhy, dependable systems, funding, publications, supervision, and academic service.",
    "Give a concise overview first, then suggest relevant pages or papers to read next."
  ].join("\n");

  const encodedPrompt = encodeURIComponent(prompt);
  const providers = [
    {
      label: "Ask ChatGPT",
      mark: "AI",
      href: "https://chatgpt.com/?q=" + encodedPrompt
    },
    {
      label: "Ask Claude",
      mark: "C",
      href: "https://claude.ai/new?q=" + encodedPrompt
    },
    {
      label: "Ask Gemini",
      mark: "G",
      href: "https://aistudio.google.com/app/prompts/new?text=" + encodedPrompt
    },
    {
      label: "Ask Kimi",
      mark: "K",
      href: "https://www.kimi.com/chat?q=" + encodedPrompt
    }
  ];

  function createProviderLink(provider) {
    const anchor = document.createElement("a");
    anchor.className = "ai-learn-panel__item";
    anchor.href = provider.href;
    anchor.target = "_blank";
    anchor.rel = "noopener";
    anchor.innerHTML = [
      '<span class="ai-learn-panel__mark">' + provider.mark + "</span>",
      "<span>" + provider.label + "</span>",
      '<span class="ai-learn-panel__external" aria-hidden="true">open</span>'
    ].join("");
    return anchor;
  }

  function mountPanel() {
    if (document.querySelector("[data-ai-learn-panel]")) {
      return;
    }

    const primaryNav = document.querySelector(".md-sidebar--primary nav.md-nav--primary");
    if (!primaryNav || !primaryNav.parentElement) {
      return;
    }

    const panel = document.createElement("section");
    panel.className = "ai-learn-panel";
    panel.setAttribute("data-ai-learn-panel", "true");

    const title = document.createElement("p");
    title.className = "ai-learn-panel__title";
    title.textContent = "Learn more with AI";

    const subtitle = document.createElement("p");
    subtitle.className = "ai-learn-panel__subtitle";
    subtitle.textContent = "Explore Koorosh's research profile, papers, grants, and supervision.";

    const list = document.createElement("div");
    list.className = "ai-learn-panel__list";
    providers.forEach(function (provider) {
      list.appendChild(createProviderLink(provider));
    });

    panel.appendChild(title);
    panel.appendChild(subtitle);
    panel.appendChild(list);
    primaryNav.parentElement.appendChild(panel);
  }

  function mountFab() {
    if (document.querySelector("[data-ai-learn-fab]")) {
      return;
    }

    const fab = document.createElement("a");
    fab.className = "ai-learn-fab";
    fab.href = providers[0].href;
    fab.target = "_blank";
    fab.rel = "noopener";
    fab.setAttribute("data-ai-learn-fab", "true");
    fab.innerHTML = '<span>Ask AI</span><span class="ai-learn-fab__dot" aria-hidden="true"></span>';
    document.body.appendChild(fab);
  }

  function mount() {
    mountPanel();
    mountFab();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(mount);
  }

  document.addEventListener("DOMContentLoaded", mount);
})();
