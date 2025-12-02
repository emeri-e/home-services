const PACKAGES = {
  essential: {
    id: "essential",
    name: "Essential Handyman",
    description: "Perfect for punch lists, light repairs, and fixture swaps you need handled fast.",
    duration: "Up to 2 hours on-site · 1 pro",
    badge: "Quick fix",
    price: 189,
    features: ["Minor plumbing & electrical", "Fixture swaps & touch-ups", "Includes trip + materials run"],
  },
  premium: {
    id: "premium",
    name: "Premium Remodel Day",
    description: "Dedicated crew for larger projects like bathroom refreshes, flooring, or multiple-room updates.",
    duration: "8-hour crew block · 2+ specialists",
    badge: "Popular",
    price: 749,
    features: ["Crew lead + coordinator updates", "Includes haul-away & cleanup", "Priority materials sourcing"],
  },
  membership: {
    id: "membership",
    name: "Total Care Membership",
    description: "Seasonal maintenance, VIP dispatching, and bundled savings for busy homeowners.",
    duration: "Annual plan · Quarterly visits",
    badge: "Membership",
    price: 129,
    billingNote: "/ month (billed annually)",
    features: ["Quarterly tune-ups", "VIP pricing on projects", "Dedicated account manager"],
  },
};

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);

const yearEl = document.getElementById("year");
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

const headerEl = document.querySelector("header");
const toggleHeaderState = () => {
  if (!headerEl) return;
  headerEl.classList.toggle("is-scrolled", window.scrollY > 4);
};
toggleHeaderState();
window.addEventListener("scroll", toggleHeaderState, { passive: true });

const motionQuery = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
const revealElements = document.querySelectorAll("[data-reveal]");

const revealAll = () => {
  revealElements.forEach((el) => {
    el.classList.add("is-visible");
  });
};

if (!motionQuery?.matches && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -40px 0px",
    }
  );

  revealElements.forEach((el) => observer.observe(el));
} else {
  revealAll();
}

motionQuery?.addEventListener("change", (event) => {
  if (event.matches) {
    revealAll();
  }
});

const smoothLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');
smoothLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    const targetId = link.getAttribute("href");
    if (!targetId || !targetId.startsWith("#")) return;
    const target = document.querySelector(targetId);
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

const initCheckoutPage = () => {
  const checkoutRoot = document.querySelector("[data-checkout-root]");
  if (!checkoutRoot) return;

  const params = new URLSearchParams(window.location.search);
  const requested = params.get("package");
  const pkg = PACKAGES[requested] || PACKAGES.essential;

  const packageNameEls = checkoutRoot.querySelectorAll("[data-package-name]");
  packageNameEls.forEach((el) => (el.textContent = pkg.name));

  const descriptionEl = checkoutRoot.querySelector("[data-package-description]");
  if (descriptionEl) descriptionEl.textContent = pkg.description;

  const durationEl = checkoutRoot.querySelector("[data-package-duration]");
  if (durationEl) durationEl.textContent = pkg.duration;

  const badgeEl = checkoutRoot.querySelector("[data-package-badge]");
  if (badgeEl) badgeEl.textContent = pkg.badge || "Selected package";

  const featuresEl = checkoutRoot.querySelector("[data-package-features]");
  if (featuresEl) {
    featuresEl.innerHTML = "";
    pkg.features.forEach((feature) => {
      const li = document.createElement("li");
      li.textContent = feature;
      featuresEl.appendChild(li);
    });
  }

  const priceEl = checkoutRoot.querySelector("[data-package-price]");
  const totalEl = checkoutRoot.querySelector("[data-package-total]");
  const addonsSummaryEl = checkoutRoot.querySelector("[data-addons-summary]");
  const addonInputs = checkoutRoot.querySelectorAll("[data-addon-price]");
  const packageInput = checkoutRoot.querySelector("[data-package-input]");
  if (packageInput) packageInput.value = pkg.id;

  const priceLabel = pkg.billingNote
    ? `${formatCurrency(pkg.price)} ${pkg.billingNote}`
    : formatCurrency(pkg.price);

  const renderTotals = () => {
    let addonTotal = 0;
    const activeAddons = [];

    addonInputs.forEach((input) => {
      if (input.checked) {
        const amount = Number(input.dataset.addonPrice) || 0;
        addonTotal += amount;
        activeAddons.push(`${input.dataset.addonLabel} (${formatCurrency(amount)})`);
      }
    });

    const total = pkg.price + addonTotal;
    if (priceEl) priceEl.textContent = priceLabel;
    if (addonsSummaryEl) {
      addonsSummaryEl.textContent = activeAddons.length ? activeAddons.join(", ") : "No add-ons selected";
    }
    if (totalEl) {
      const totalLabel = pkg.billingNote
        ? `${formatCurrency(total)} ${pkg.billingNote}`
        : formatCurrency(total);
      totalEl.textContent = totalLabel;
    }
  };

  addonInputs.forEach((input) => {
    input.addEventListener("change", renderTotals);
  });

  renderTotals();
};

document.addEventListener("DOMContentLoaded", initCheckoutPage);

