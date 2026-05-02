import { useEffect, useRef, useState } from "react";

const DEFAULT_WS_BASE = "http://localhost:8000";

const buildWsUrl = (role, token) => {
  const configured = import.meta.env.VITE_WS_URL || import.meta.env.VITE_API_URL || DEFAULT_WS_BASE;
  const base = configured.replace(/\/api\/v1\/?$/, "").replace(/^http/, "ws");
  return `${base}/ws/${role}?token=${encodeURIComponent(token)}`;
};

const pushLimited = (items, nextItem, limit = 20) => [...items, nextItem].slice(-limit);

export function useAgroWebSocket(role, token) {
  const [connected, setConnected] = useState(false);
  const [weather, setWeather] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [pestAlerts, setPestAlerts] = useState([]);
  const [adminSnapshot, setAdminSnapshot] = useState(null);
  const [liveEvents, setLiveEvents] = useState([]);
  const [error, setError] = useState("");

  const socketRef = useRef(null);
  const reconnectRef = useRef(null);
  const predictionTimerRef = useRef(null);
  const latestInputsRef = useRef(null);
  const activeRef = useRef(true);

  const send = (payload) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(payload));
    }
  };

  const connect = () => {
    if (!token) {
      setConnected(false);
      return;
    }

    const socket = new WebSocket(buildWsUrl(role, token));
    socketRef.current = socket;

    socket.onopen = () => {
      if (!activeRef.current) {
        socket.close();
        return;
      }
      setConnected(true);
      setError("");
    };

    socket.onmessage = (event) => {
      let payload;
      try {
        payload = JSON.parse(event.data);
      } catch {
        return;
      }

      if (payload.type === "connected") {
        setConnected(true);
        if (payload.weather) {
          setWeather(payload.weather);
        }
        return;
      }

      if (payload.type === "weather_update") {
        setWeather(payload);
        return;
      }

      if (payload.type === "yield_prediction") {
        setPrediction(payload.result || payload);
        return;
      }

      if (payload.type === "pest_alert") {
        setPestAlerts(payload.alerts || []);
        return;
      }

      if (payload.type === "admin_snapshot") {
        setAdminSnapshot(payload);
        return;
      }

      if (payload.type === "live_event" || payload.type === "admin_event") {
        setLiveEvents((items) => pushLimited(items, payload));
      }
    };

    socket.onerror = () => {
      setError("Realtime connection error");
    };

    socket.onclose = () => {
      setConnected(false);
      if (activeRef.current && token) {
        reconnectRef.current = window.setTimeout(connect, 3000);
      }
    };
  };

  useEffect(() => {
    activeRef.current = true;
    connect();

    return () => {
      activeRef.current = false;
      setConnected(false);
      if (predictionTimerRef.current) {
        window.clearTimeout(predictionTimerRef.current);
      }
      if (reconnectRef.current) {
        window.clearTimeout(reconnectRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [role, token]);

  const sendPredictionInputs = (inputs) => {
    latestInputsRef.current = inputs;
    if (predictionTimerRef.current) {
      window.clearTimeout(predictionTimerRef.current);
    }
    predictionTimerRef.current = window.setTimeout(() => {
      send({ action: "predict", inputs: latestInputsRef.current });
    }, 300);
  };

  const checkPests = (crops = []) => send({ action: "check_pests", crops });
  const subscribeWeather = (district) => send({ action: "subscribe_weather", district });
  const requestSnapshot = () => send({ action: "get_snapshot" });
  const broadcastAlert = (district, message) => send({ action: "broadcast_alert", district, message });
  const ping = () => send({ action: "ping" });

  return {
    connected,
    error,
    weather,
    prediction,
    pestAlerts,
    adminSnapshot,
    liveEvents,
    sendPredictionInputs,
    checkPests,
    subscribeWeather,
    requestSnapshot,
    broadcastAlert,
    ping,
  };
}
