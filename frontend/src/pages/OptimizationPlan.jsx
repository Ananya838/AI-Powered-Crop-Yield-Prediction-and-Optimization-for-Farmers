import { useState } from "react";
import { useTranslation } from "react-i18next";
import { api, authHeader } from "../api/client";

const payload = {
  crop: "wheat",
  district: "Pune",
  village: "Hinjawadi",
  rainfall: 640,
  temperature: 27,
  nitrogen: 70,
  phosphorus: 32,
  potassium: 28,
  ph: 6.5,
  irrigation: "canal",
  season: "kharif"
};

export default function OptimizationPlan() {
  const { t } = useTranslation();
  const [plan, setPlan] = useState(null);

  const fetchPlan = async () => {
    const { data } = await api.post("/optimization/plan", payload, { headers: authHeader() });
    setPlan(data);
  };

  return (
    <section className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-display text-xl">{t("plan.title")}</h2>
        <button onClick={fetchPlan} className="rounded-xl bg-sky text-white px-4 py-2">{t("plan.generate")}</button>
      </div>
      {!plan ? (
        <p>{t("plan.empty")}</p>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold">{t("plan.irrigation")}</h3>
            <ul className="list-disc ml-5 text-sm">{plan.irrigation_schedule.map((i) => <li key={i}>{i}</li>)}</ul>
          </div>
          <div>
            <h3 className="font-semibold">{t("plan.fertilizer")}</h3>
            <ul className="list-disc ml-5 text-sm">{plan.fertilizer_dosage.map((i) => <li key={i}>{i}</li>)}</ul>
          </div>
          <div>
            <h3 className="font-semibold">{t("plan.pest")}</h3>
            <ul className="list-disc ml-5 text-sm">{plan.pest_prevention.map((i) => <li key={i}>{i}</li>)}</ul>
          </div>
          <div>
            <h3 className="font-semibold">{t("plan.disease")}</h3>
            <ul className="list-disc ml-5 text-sm">{plan.disease_risk_alerts.map((i) => <li key={i}>{i}</li>)}</ul>
          </div>
          <p className="md:col-span-2">{t("plan.gain")}: <b>{plan.expected_gain_percent}%</b></p>
        </div>
      )}
    </section>
  );
}
