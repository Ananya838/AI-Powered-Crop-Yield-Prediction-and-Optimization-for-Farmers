import { useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useTranslation } from "react-i18next";
import { api, authHeader } from "../api/client";
import { useAgroWebSocket } from "../hooks/useAgroWebSocket";

const initial = {
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

export default function YieldPrediction() {
  const { t } = useTranslation();
  const [form, setForm] = useState(initial);
  const [result, setResult] = useState(null);
  const [lat, setLat] = useState(18.52);
  const [lon, setLon] = useState(73.85);
  const [soilLoading, setSoilLoading] = useState(false);
  const [soilMessage, setSoilMessage] = useState("");
  const [soilInputMode, setSoilInputMode] = useState("geo"); // "geo" or "district"
  const token = localStorage.getItem("token");
  const { connected, prediction: livePrediction, sendPredictionInputs, weather } = useAgroWebSocket("farmer", token);
  const activeResult = livePrediction || result;

  const explainabilityData = (activeResult?.explainability || []).slice(0, 6).map((item) => ({
    feature: item.feature,
    impact: Number(item.impact),
    signedImpact: item.direction === "negative" ? -Math.abs(Number(item.impact)) : Math.abs(Number(item.impact))
  }));

  const onChange = (k, v) => {
    const nextForm = { ...form, [k]: ["rainfall", "temperature", "nitrogen", "phosphorus", "potassium", "ph"].includes(k) ? Number(v) : v };
    setForm(nextForm);
    sendPredictionInputs(nextForm);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const { data } = await api.post("/prediction/yield", form, { headers: authHeader() });
    setResult(data);
  };

  const autofillSoil = async () => {
    setSoilLoading(true);
    setSoilMessage("");

    try {
      const { data } = await api.get("/data/soil", {
        params: { latitude: Number(lat), longitude: Number(lon) },
        headers: authHeader()
      });

      setForm((prev) => ({
        ...prev,
        nitrogen: Number(data.nitrogen),
        phosphorus: Number(data.estimated_phosphorus),
        potassium: Number(data.estimated_potassium),
        ph: Number(data.ph)
      }));

      setSoilMessage(`${t("soilAssist.success")} (${t("common.source")}: ${data.source})`);
    } catch {
      setSoilMessage(t("soilAssist.error"));
    } finally {
      setSoilLoading(false);
    }
  };

  const autofillSoilByDistrict = async () => {
    setSoilLoading(true);
    setSoilMessage("");

    try {
      const { data } = await api.get("/data/soil-by-district", {
        params: { district: form.district },
        headers: authHeader()
      });

      setForm((prev) => ({
        ...prev,
        nitrogen: Number(data.nitrogen),
        phosphorus: Number(data.estimated_phosphorus),
        potassium: Number(data.estimated_potassium),
        ph: Number(data.ph)
      }));

      setSoilMessage(`${t("soilAssist.success")} (${t("common.source")}: ${data.source})`);
    } catch {
      setSoilMessage(t("soilAssist.error"));
    } finally {
      setSoilLoading(false);
    }
  };

  const useCurrentLocation = () => {
    if (!navigator.geolocation) {
      setSoilMessage(t("soilAssist.geoUnavailable"));
      return;
    }

    setSoilMessage("");
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLat(position.coords.latitude.toFixed(4));
        setLon(position.coords.longitude.toFixed(4));
        setSoilMessage(t("soilAssist.geoSuccess"));
      },
      () => setSoilMessage(t("soilAssist.geoError")),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
    );
  };

  return (
    <section className="grid lg:grid-cols-2 gap-6">
      <form className="card grid grid-cols-2 gap-3" onSubmit={onSubmit}>
        <div className="col-span-2 flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-700">
          <span>{connected ? "Live prediction connected" : "Live prediction offline"}</span>
          <span>{weather ? `${weather.district || form.district} | ${weather.current?.temperature_c ?? "--"}°C` : "Waiting for weather stream"}</span>
        </div>
        <div className="col-span-2 rounded-xl border border-slate-200 bg-slate-50 p-3">
          <p className="text-sm font-semibold">{t("soilAssist.title")}</p>
          <p className="text-xs text-slate-600 mt-1">{t("soilAssist.desc")}</p>
          
          {/* Mode selector */}
          <div className="mt-3 flex gap-2 border-b border-slate-300">
            <button
              type="button"
              onClick={() => setSoilInputMode("geo")}
              className={`px-3 py-2 text-xs font-medium border-b-2 ${soilInputMode === "geo" ? "border-sky text-sky" : "border-transparent text-slate-600"}`}
            >
              {t("soilAssist.geoButton")}
            </button>
            <button
              type="button"
              onClick={() => setSoilInputMode("district")}
              className={`px-3 py-2 text-xs font-medium border-b-2 ${soilInputMode === "district" ? "border-sky text-sky" : "border-transparent text-slate-600"}`}
            >
              {t("soilAssist.districtButton")}
            </button>
          </div>

          {/* Geolocation mode */}
          {soilInputMode === "geo" && (
            <>
              <div className="mt-3 grid grid-cols-2 gap-2">
                <label className="text-sm">
                  <span className="block mb-1">{t("soilAssist.lat")}</span>
                  <input className="w-full rounded-lg border border-slate-300 px-2 py-2" value={lat} onChange={(e) => setLat(e.target.value)} />
                </label>
                <label className="text-sm">
                  <span className="block mb-1">{t("soilAssist.lon")}</span>
                  <input className="w-full rounded-lg border border-slate-300 px-2 py-2" value={lon} onChange={(e) => setLon(e.target.value)} />
                </label>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                <button type="button" onClick={useCurrentLocation} className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-100">
                  {t("soilAssist.geoButton")}
                </button>
                <button type="button" onClick={autofillSoil} className="rounded-lg bg-sky text-white px-3 py-2 text-sm hover:bg-sky-600">
                  {soilLoading ? t("soilAssist.loading") : t("soilAssist.fetch")}
                </button>
              </div>
            </>
          )}

          {/* District mode */}
          {soilInputMode === "district" && (
            <>
              <div className="mt-3">
                <label className="text-sm">
                  <span className="block mb-1">{t("fields.district")}</span>
                  <select className="w-full rounded-lg border border-slate-300 px-2 py-2" value={form.district} onChange={(e) => onChange("district", e.target.value)}>
                    <option value="Pune">Pune</option>
                    <option value="Nashik">Nashik</option>
                    <option value="Nagpur">Nagpur</option>
                    <option value="Solapur">Solapur</option>
                  </select>
                </label>
              </div>
              <div className="mt-3">
                <button type="button" onClick={autofillSoilByDistrict} className="w-full rounded-lg bg-leaf text-white px-3 py-2 text-sm hover:bg-leaf-700">
                  {soilLoading ? t("soilAssist.loading") : t("soilAssist.districtFetch")}
                </button>
              </div>
            </>
          )}

          {soilMessage ? <p className="text-xs text-slate-700 mt-2">{soilMessage}</p> : null}
        </div>

        {Object.keys(form).map((key) => (
          <label key={key} className="text-sm">
            <span className="block mb-1">{t(`fields.${key}`)}</span>
            <input
              className="w-full rounded-lg border border-slate-300 px-2 py-2"
              value={form[key]}
              onChange={(e) => onChange(key, e.target.value)}
            />
          </label>
        ))}
        <button className="col-span-2 rounded-xl bg-leaf text-white py-2 font-semibold">{t("yield.submit")}</button>
      </form>

      <div className="card min-h-[420px]">
        <h3 className="font-display text-lg">{t("yield.title")}</h3>
        {!activeResult ? (
          <p className="text-slate-600 mt-4">{t("yield.empty")}</p>
        ) : (
          <>
            {livePrediction?.generated_at ? <p className="text-xs uppercase tracking-[0.2em] text-sky-700">Realtime</p> : null}
            <p className="mt-4">{t("yield.expected")}: <b>{activeResult.expected_yield} t/ha</b></p>
            <p>{t("yield.confidence")}: <b>{activeResult.confidence_score}</b></p>
            <p>{t("yield.suggested")}: <b>{activeResult.suggested_crop}</b></p>
            <div className="mt-4">
              <h4 className="font-semibold">{t("yield.explain")}</h4>
              <div className="space-y-2 mt-2">
                {(activeResult.explainability || []).slice(0, 5).map((item) => (
                  <div key={item.feature} className="rounded-lg border border-slate-200 p-2 bg-white/70 text-sm flex items-center justify-between">
                    <span className="capitalize">{item.feature}</span>
                    <span className={item.direction === "positive" ? "text-green-700 font-semibold" : "text-red-700 font-semibold"}>
                      {item.direction} ({item.impact})
                    </span>
                  </div>
                ))}
              </div>
              <div className="h-[220px] mt-3 rounded-xl border border-slate-100 bg-white/70 p-2">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={explainabilityData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="feature" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="signedImpact" radius={[6, 6, 0, 0]}>
                      {explainabilityData.map((entry) => (
                        <Cell key={entry.feature} fill={entry.signedImpact >= 0 ? "#2f7d32" : "#c62828"} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div className="h-[240px] mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={activeResult.yield_trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip />
                  <Line dataKey="yield" stroke="#1e88e5" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </div>
    </section>
  );
}
