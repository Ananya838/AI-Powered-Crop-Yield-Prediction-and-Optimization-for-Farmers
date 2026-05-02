import { useTranslation } from "react-i18next";

export default function LandingPage() {
  const { t } = useTranslation();

  return (
    <section className="relative overflow-hidden rounded-3xl py-6 px-1">
      <div className="hero-blob hero-blob-a" />
      <div className="hero-blob hero-blob-b" />

      <div className="relative grid md:grid-cols-2 gap-6 items-start">
        <div className="card fade-in-up" style={{ animationDelay: "0.05s" }}>
          <p className="inline-flex items-center gap-2 text-xs uppercase tracking-wide bg-leaf/10 text-leaf px-3 py-1 rounded-full">
            SIH 2025 Ready
          </p>
          <h2 className="font-display text-3xl lg:text-4xl text-slate-800 mt-3">{t("landing.title")}</h2>
          <p className="mt-3 text-slate-700">{t("landing.desc")}</p>

          <div className="mt-5 grid sm:grid-cols-3 gap-3 text-sm">
            <div className="rounded-xl bg-leaf/10 border border-leaf/20 p-3">{t("landing.impact")}</div>
            <div className="rounded-xl bg-sky/10 border border-sky/20 p-3">{t("landing.multi")}</div>
            <div className="rounded-xl bg-sun/15 border border-sun/30 p-3">{t("landing.data")}</div>
          </div>
        </div>

        <div className="card fade-in-up" style={{ animationDelay: "0.15s" }}>
          <div className="relative">
            <img
              className="rounded-xl w-full h-[290px] object-cover floating-image"
              src="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1000&q=80"
              alt="farm"
            />
            <div className="absolute -bottom-3 -right-2 bg-white/90 border border-white rounded-lg px-3 py-2 shadow text-xs font-semibold text-slate-700">
              AI + Soil + Weather
            </div>
          </div>
        </div>
      </div>

      <div className="relative card md:col-span-2 mt-6 fade-in-up" style={{ animationDelay: "0.25s" }}>
        <h3 className="font-display text-xl">{t("landing.stepsTitle")}</h3>
        <ol className="mt-4 grid md:grid-cols-2 gap-3 text-sm">
          <li className="rounded-xl bg-white/80 border border-slate-100 p-3">1. {t("landing.s1")}</li>
          <li className="rounded-xl bg-white/80 border border-slate-100 p-3">2. {t("landing.s2")}</li>
          <li className="rounded-xl bg-white/80 border border-slate-100 p-3">3. {t("landing.s3")}</li>
          <li className="rounded-xl bg-white/80 border border-slate-100 p-3">4. {t("landing.s4")}</li>
          <li className="rounded-xl bg-white/80 border border-slate-100 p-3 md:col-span-2">5. {t("landing.s5")}</li>
        </ol>
      </div>
    </section>
  );
}
