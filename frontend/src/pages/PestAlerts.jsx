import { useTranslation } from "react-i18next";

const alerts = [
  { district: "Pune", risk: "Medium", action: "Scout twice weekly" },
  { district: "Nashik", risk: "High", action: "Deploy pheromone traps" },
  { district: "Nagpur", risk: "Low", action: "Preventive neem spray" }
];

export default function PestAlerts() {
  const { t } = useTranslation();

  return (
    <section className="card">
      <h2 className="font-display text-xl mb-4">{t("pest.title")}</h2>
      <div className="space-y-3">
        {alerts.map((a) => (
          <div key={a.district} className="rounded-xl border border-slate-200 p-3 bg-white/70">
            <p className="font-semibold">{a.district}: {a.risk}</p>
            <p className="text-sm text-slate-700">{a.action}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
