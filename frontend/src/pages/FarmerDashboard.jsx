import { BarChart, Bar, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import StatCard from "../components/StatCard";
import { useAgroWebSocket } from "../hooks/useAgroWebSocket";

const data = [
  { month: "Jan", yield: 2.2 },
  { month: "Feb", yield: 2.4 },
  { month: "Mar", yield: 2.8 },
  { month: "Apr", yield: 3.1 }
];

export default function FarmerDashboard() {
  const { t } = useTranslation();
  const [district, setDistrict] = useState("pune");
  const token = localStorage.getItem("token");
  const { connected, weather, pestAlerts, subscribeWeather, checkPests } = useAgroWebSocket("farmer", token);

  useEffect(() => {
    if (connected) {
      subscribeWeather(district);
    }
  }, [connected, district]);

  return (
    <section className="space-y-5">
      <div className="card flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Realtime feed</p>
          <h2 className="font-display text-xl">{connected ? "Live" : "Offline"}</h2>
        </div>
        <div className="flex items-center gap-3">
          <select className="rounded-lg border border-slate-300 px-3 py-2" value={district} onChange={(e) => setDistrict(e.target.value)}>
            <option value="pune">Pune</option>
            <option value="nashik">Nashik</option>
            <option value="nagpur">Nagpur</option>
            <option value="solapur">Solapur</option>
          </select>
          <button type="button" className="rounded-lg bg-leaf px-3 py-2 text-white" onClick={() => checkPests(["wheat", "rice"])}>
            Check pests
          </button>
        </div>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        <StatCard label={t("dash.predicted")} value={weather ? `${weather.current?.temperature_c ?? 0}°C` : "3.2 t/ha"} hint={weather ? weather.irrigation_advice : t("dash.confidence")} />
        <StatCard label={t("dash.water")} value="18%" hint={t("dash.waterHint")} />
        <StatCard label={t("dash.pest")} value={pestAlerts.length ? pestAlerts[0].severity : "Medium"} hint={pestAlerts.length ? pestAlerts[0].name : t("dash.pestHint")} />
      </div>
      <div className="card">
        <h3 className="font-display text-lg mb-2">Weather Update</h3>
        {weather ? (
          <div className="grid md:grid-cols-3 gap-3 text-sm">
            <div>Temperature: <b>{weather.current?.temperature_c ?? "--"}°C</b></div>
            <div>Humidity: <b>{weather.current?.humidity_pct ?? "--"}%</b></div>
            <div>Rainfall: <b>{weather.current?.rainfall_mm ?? "--"} mm</b></div>
          </div>
        ) : (
          <p className="text-slate-600">Waiting for live weather updates...</p>
        )}
      </div>
      <div className="card">
        <h3 className="font-display text-lg mb-2">Active pest alerts</h3>
        {pestAlerts.length ? (
          <ul className="space-y-2 text-sm">
            {pestAlerts.map((alert) => (
              <li key={alert.rule_id} className="rounded-lg border border-slate-200 bg-white/70 p-2">
                <div className="font-semibold">{alert.name}</div>
                <div className="text-slate-600">{alert.action}</div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-600">No active alerts right now.</p>
        )}
      </div>
      <div className="card h-[340px]">
        <h3 className="font-display text-lg mb-2">{t("dash.trend")}</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="yield" fill="#2f7d32" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
