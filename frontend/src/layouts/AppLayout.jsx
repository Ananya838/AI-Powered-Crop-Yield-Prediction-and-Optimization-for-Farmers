import { NavLink, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { clearAuthToken } from "../api/client";

const navItems = [
  ["/", "nav.landing"],
  ["/auth", "nav.auth"],
  ["/dashboard", "nav.dashboard"],
  ["/yield", "nav.yield"],
  ["/soil", "nav.soil"],
  ["/weather", "nav.weather"],
  ["/pest", "nav.pest"],
  ["/plan", "nav.plan"],
  ["/admin", "nav.admin"]
];

export default function AppLayout() {
  const { t, i18n } = useTranslation();
  const [loggedIn, setLoggedIn] = useState(Boolean(localStorage.getItem("token")));

  useEffect(() => {
    const handler = () => setLoggedIn(Boolean(localStorage.getItem("token")));
    window.addEventListener("auth-updated", handler);
    return () => window.removeEventListener("auth-updated", handler);
  }, []);

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-white/70 bg-white/80 backdrop-blur">
        <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between gap-3">
          <div>
            <h1 className="font-display text-xl text-leaf">{t("appTitle")}</h1>
            <p className="text-sm text-slate-600">{t("subtitle")}</p>
          </div>
          <select
            className="rounded-lg border border-slate-300 px-2 py-1"
            value={i18n.language}
            onChange={(e) => i18n.changeLanguage(e.target.value)}
          >
            <option value="en">{t("lang.en")}</option>
            <option value="hi">{t("lang.hi")}</option>
            <option value="mr">{t("lang.mr")}</option>
            <option value="kn">{t("lang.kn")}</option>
          </select>
          {loggedIn ? (
            <button onClick={clearAuthToken} className="rounded-lg bg-rose-600 text-white px-3 py-1 text-sm">{t("auth.logout")}</button>
          ) : null}
        </div>
      </header>

      <nav className="mx-auto max-w-7xl px-4 py-3 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-9 gap-2 text-sm">
        {navItems.map(([to, key]) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `rounded-xl px-3 py-2 text-center transition ${isActive ? "bg-leaf text-white" : "bg-white/70 hover:bg-white"}`
            }
          >
            {t(key)}
          </NavLink>
        ))}
      </nav>

      <main className="mx-auto max-w-7xl px-4 pb-8">
        <Outlet />
      </main>
    </div>
  );
}
