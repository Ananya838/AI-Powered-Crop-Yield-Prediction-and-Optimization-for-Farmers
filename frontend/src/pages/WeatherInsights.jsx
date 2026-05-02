import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { AreaChart, Area, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api, authHeader } from "../api/client";

const rain = [
  { week: "W1", rain: 42 },
  { week: "W2", rain: 54 },
  { week: "W3", rain: 49 },
  { week: "W4", rain: 58 }
];

export default function WeatherInsights() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get("/data/weather", {
          params: { district: "Pune", season: "kharif" },
          headers: authHeader()
        });
        setSummary(data);
      } catch {
        setSummary(null);
      }
    };
    load();
  }, []);

  return (
    <section className="card h-[380px]">
      <h2 className="font-display text-xl">{t("weather.title")}</h2>
      <p className="text-sm text-slate-600 mb-3">{t("weather.desc")}</p>
      {summary ? (
        <p className="text-xs text-slate-700 mb-2">
          {t("weather.live")} - {t("fields.rainfall")}: {summary.avg_rainfall_mm} mm/day, {t("fields.temperature")}: {summary.avg_temperature_c} C, {t("common.source")}: {summary.source}
        </p>
      ) : null}
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={rain}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="week" />
          <YAxis />
          <Tooltip />
          <Area dataKey="rain" type="monotone" fill="#1e88e5" stroke="#1e88e5" fillOpacity={0.35} />
        </AreaChart>
      </ResponsiveContainer>
    </section>
  );
}
