import { useTranslation } from "react-i18next";

const rows = [
  ["Nitrogen", "70 kg/ha", "Optimal"],
  ["Phosphorus", "32 kg/ha", "Moderate"],
  ["Potassium", "28 kg/ha", "Low"],
  ["pH", "6.5", "Healthy"]
];

export default function SoilHealth() {
  const { t } = useTranslation();

  return (
    <section className="card">
      <h2 className="font-display text-xl mb-4">{t("soil.title")}</h2>
      <div className="overflow-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">{t("soil.parameter")}</th>
              <th>{t("soil.value")}</th>
              <th>{t("soil.status")}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(([p, v, s]) => (
              <tr key={p} className="border-b border-slate-100">
                <td className="py-2">{p}</td>
                <td>{v}</td>
                <td>{s}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
