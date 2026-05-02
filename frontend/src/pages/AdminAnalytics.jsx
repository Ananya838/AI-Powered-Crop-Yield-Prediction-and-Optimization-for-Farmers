import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useTranslation } from "react-i18next";
import { api, authHeader } from "../api/client";
import { useAgroWebSocket } from "../hooks/useAgroWebSocket";

const adoption = [
  { name: "Pune", value: 620 },
  { name: "Nashik", value: 510 },
  { name: "Nagpur", value: 390 }
];

const colors = ["#2f7d32", "#1e88e5", "#f4b400"];

const fallback = {
  district_heatmap: [
    { district: "Pune", productivity_index: 78.2 },
    { district: "Nashik", productivity_index: 82.4 },
    { district: "Nagpur", productivity_index: 69.7 }
  ],
  productivity_report: [
    { month: "Y2022", avg_yield: 2.6 },
    { month: "Y2023", avg_yield: 2.9 },
    { month: "Y2024", avg_yield: 3.2 }
  ],
  crop_failure_alerts: [
    { district: "Nagpur", alerts: 4 },
    { district: "Solapur", alerts: 2 }
  ],
  farmer_adoption: adoption.map((a) => ({ district: a.name, active_farmers: a.value }))
};

export default function AdminAnalytics() {
  const { t } = useTranslation();
  const [analytics, setAnalytics] = useState(fallback);
  const token = localStorage.getItem("token");
  const { connected, adminSnapshot, liveEvents, requestSnapshot, broadcastAlert } = useAgroWebSocket("admin", token);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get("/admin/analytics", { headers: authHeader() });
        setAnalytics(data);
      } catch {
        setAnalytics(fallback);
      }
    };
    load();
  }, []);

  useEffect(() => {
    if (connected) {
      requestSnapshot();
    }
  }, [connected]);

  const liveSnapshot = adminSnapshot || { active_events: 0, districts: [], critical_alerts: [], recent_events: [] };

  const adoptionData = analytics.farmer_adoption.map((item) => ({ name: item.district, value: item.active_farmers }));

  return (
    <section className="grid lg:grid-cols-2 gap-5">
      <div className="card lg:col-span-2 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Realtime admin feed</p>
          <h2 className="font-display text-xl">{connected ? "Live connected" : "Offline"}</h2>
        </div>
        <button type="button" className="rounded-lg bg-sky px-3 py-2 text-white" onClick={() => broadcastAlert("pune", "Admin broadcast from dashboard")}>Broadcast test alert</button>
      </div>
      <div className="card lg:col-span-2">
        <h2 className="font-display text-xl">Live snapshot</h2>
        <div className="mt-3 grid gap-3 md:grid-cols-3 text-sm">
          <div className="rounded-xl border border-slate-200 bg-white/70 p-3">Active events: <b>{liveSnapshot.active_events}</b></div>
          <div className="rounded-xl border border-slate-200 bg-white/70 p-3">Districts: <b>{liveSnapshot.districts.map(([district]) => district).join(", ") || "N/A"}</b></div>
          <div className="rounded-xl border border-slate-200 bg-white/70 p-3">Critical alerts: <b>{liveSnapshot.critical_alerts.length}</b></div>
        </div>
        <div className="mt-4 rounded-xl border border-slate-200 bg-white/70 p-3 text-sm">
          <p className="font-semibold mb-2">Recent events</p>
          <ul className="space-y-1">
            {(liveEvents.slice(-5).reverse()).map((event, index) => (
              <li key={`${event.type}-${index}`}>{event.type} {event.district ? `| ${event.district}` : ""}</li>
            ))}
            {!liveEvents.length ? <li>No live events yet.</li> : null}
          </ul>
        </div>
      </div>
      <div className="card h-[320px]">
        <h2 className="font-display text-xl">{t("admin.title1")}</h2>
        <ResponsiveContainer width="100%" height="90%">
          <PieChart>
            <Pie data={adoptionData} dataKey="value" nameKey="name" outerRadius={100}>
              {adoptionData.map((_, idx) => (
                <Cell key={idx} fill={colors[idx % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="card">
        <h2 className="font-display text-xl">{t("admin.title2")}</h2>
        <ul className="mt-3 space-y-2 text-sm">
          {analytics.district_heatmap.map((item) => (
            <li key={item.district}>{item.district}: {t("admin.productivityIndex")} {item.productivity_index}</li>
          ))}
          <li>{t("admin.hotspot")}: {(analytics.crop_failure_alerts[0] || {}).district || "N/A"}</li>
        </ul>
      </div>
      <div className="card lg:col-span-2 h-[280px]">
        <h2 className="font-display text-xl">{t("admin.title3")}</h2>
        <ResponsiveContainer width="100%" height="86%">
          <BarChart data={analytics.productivity_report}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="avg_yield" fill="#1e88e5" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
