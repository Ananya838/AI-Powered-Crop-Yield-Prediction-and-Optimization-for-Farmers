import "./styles/index.css";
import "./i18n";
import { lazy, Suspense } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useTranslation } from "react-i18next";

import AppLayout from "./layouts/AppLayout";

const LandingPage = lazy(() => import("./pages/LandingPage"));
const FarmerDashboard = lazy(() => import("./pages/FarmerDashboard"));
const YieldPrediction = lazy(() => import("./pages/YieldPrediction"));
const SoilHealth = lazy(() => import("./pages/SoilHealth"));
const WeatherInsights = lazy(() => import("./pages/WeatherInsights"));
const PestAlerts = lazy(() => import("./pages/PestAlerts"));
const OptimizationPlan = lazy(() => import("./pages/OptimizationPlan"));
const AdminAnalytics = lazy(() => import("./pages/AdminAnalytics"));
const AuthPage = lazy(() => import("./pages/AuthPage"));

export default function App() {
  const { t } = useTranslation();

  return (
    <BrowserRouter>
      <Suspense fallback={<div className="px-4 py-10 text-center text-slate-700">{t("common.loading")}</div>}>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route path="/dashboard" element={<FarmerDashboard />} />
            <Route path="/yield" element={<YieldPrediction />} />
            <Route path="/soil" element={<SoilHealth />} />
            <Route path="/weather" element={<WeatherInsights />} />
            <Route path="/pest" element={<PestAlerts />} />
            <Route path="/plan" element={<OptimizationPlan />} />
            <Route path="/admin" element={<AdminAnalytics />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
