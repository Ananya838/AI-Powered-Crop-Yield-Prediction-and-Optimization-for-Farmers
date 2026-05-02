import { useState } from "react";
import { useTranslation } from "react-i18next";
import { api, setAuthToken } from "../api/client";

export default function AuthPage() {
  const { t } = useTranslation();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({
    full_name: "",
    phone: "",
    password: "",
    language: "en"
  });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const onChange = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      if (mode === "register") {
        await api.post("/auth/register", {
          full_name: form.full_name,
          phone: form.phone,
          password: form.password,
          language: form.language
        });
      }

      const { data } = await api.post("/auth/login", {
        phone: form.phone,
        password: form.password
      });
      setAuthToken(data.access_token);
      setMessage(t("auth.success"));
    } catch {
      setMessage(t("auth.error"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="grid md:grid-cols-2 gap-6 py-6">
      <div className="card">
        <h2 className="font-display text-2xl">{t("auth.title")}</h2>
        <p className="text-sm text-slate-700 mt-2">{t("auth.desc")}</p>
        <ol className="mt-4 space-y-2 text-sm list-decimal ml-5">
          <li>{t("auth.step1")}</li>
          <li>{t("auth.step2")}</li>
          <li>{t("auth.step3")}</li>
        </ol>
      </div>

      <form className="card space-y-3" onSubmit={onSubmit}>
        <div className="flex gap-2">
          <button type="button" onClick={() => setMode("login")} className={`px-3 py-2 rounded-lg ${mode === "login" ? "bg-leaf text-white" : "bg-slate-100"}`}>
            {t("auth.login")}
          </button>
          <button type="button" onClick={() => setMode("register")} className={`px-3 py-2 rounded-lg ${mode === "register" ? "bg-leaf text-white" : "bg-slate-100"}`}>
            {t("auth.register")}
          </button>
        </div>

        {mode === "register" ? (
          <label className="block text-sm">
            <span className="block mb-1">{t("auth.fullName")}</span>
            <input className="w-full rounded-lg border border-slate-300 px-3 py-2" value={form.full_name} onChange={(e) => onChange("full_name", e.target.value)} required />
          </label>
        ) : null}

        <label className="block text-sm">
          <span className="block mb-1">{t("auth.phone")}</span>
          <input className="w-full rounded-lg border border-slate-300 px-3 py-2" value={form.phone} onChange={(e) => onChange("phone", e.target.value)} required />
        </label>

        <label className="block text-sm">
          <span className="block mb-1">{t("auth.password")}</span>
          <input type="password" className="w-full rounded-lg border border-slate-300 px-3 py-2" value={form.password} onChange={(e) => onChange("password", e.target.value)} required />
        </label>

        {mode === "register" ? (
          <label className="block text-sm">
            <span className="block mb-1">{t("auth.prefLanguage")}</span>
            <select className="w-full rounded-lg border border-slate-300 px-3 py-2" value={form.language} onChange={(e) => onChange("language", e.target.value)}>
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="mr">Marathi</option>
              <option value="kn">Kannada</option>
            </select>
          </label>
        ) : null}

        <button disabled={loading} className="w-full rounded-xl bg-sky text-white py-2 font-semibold">
          {loading ? t("auth.working") : mode === "login" ? t("auth.login") : t("auth.register")}
        </button>

        {message ? <p className="text-sm text-slate-700">{message}</p> : null}
      </form>
    </section>
  );
}
