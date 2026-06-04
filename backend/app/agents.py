from typing import List, Dict, Generator
import random
import os
from langchain.llms import OpenAI


class SensorAnalysisAgent:
    def analyze(self, sensor_data: Dict) -> Dict:
        # Simple threshold-based checks; replace with model-based analysis
        alerts = []
        for k, v in sensor_data.items():
            if isinstance(v, (int, float)):
                if v > 100:
                    alerts.append(f"{k} high: {v}")
        return {"alerts": alerts, "summary": "sensor scan complete"}


class FaultDiagnosisAgent:
    def diagnose(self, symptoms: str, context_docs: List[Dict]) -> Dict:
        # Placeholder: call an LLM to interpret symptoms and docs
        llm = OpenAI(temperature=0)
        prompt = f"Interpret symptoms: {symptoms}\nContext: {context_docs[:2]}"
        summary = llm(prompt)
        return {"diagnosis": summary, "confidence": random.uniform(0.6, 0.95)}


class MaintenanceHistoryAgent:
    def query_history(self, query: str) -> Dict:
        # Placeholder: integrate with DB; for now return mock
        return {"matches": [], "note": "no prior incidents found"}


class SparePartsAgent:
    def recommend(self, diagnosis: str) -> Dict:
        # Simple mapping heuristic
        parts = ["motor", "bearing"] if "motor" in diagnosis.lower() else ["inspect assembly"]
        return {"parts": parts, "estimated_downtime_hours": 2}


class SupervisorAgent:
    def __init__(self):
        self.sensor = SensorAnalysisAgent()
        self.diagnosis = FaultDiagnosisAgent()
        self.history = MaintenanceHistoryAgent()
        self.spare = SparePartsAgent()

    def run(self, query: str, sensor_data: Dict, docs: List[Dict]) -> Dict:
        s = self.sensor.analyze(sensor_data)
        d = self.diagnosis.diagnose(query, docs)
        h = self.history.query_history(query)
        sp = self.spare.recommend(d.get('diagnosis', ''))
        return {
            "sensor_analysis": s,
            "diagnosis": d,
            "history": h,
            "spare_parts": sp,
            "final_report": f"Diagnosis: {d.get('diagnosis')[:200]}..."
        }

    def run_streaming(self, query: str, sensor_data: Dict, docs: List[Dict]) -> Generator[Dict, None, None]:
        yield {"status": "sensor_analysis_started"}
        yield {"sensor_analysis": self.sensor.analyze(sensor_data)}
        yield {"status": "diagnosis_started"}
        yield {"diagnosis_partial": "running LLM..."}
        diag = self.diagnosis.diagnose(query, docs)
        yield {"diagnosis": diag}
        yield {"status": "history_check"}
        yield {"history": self.history.query_history(query)}
        yield {"status": "spare_recommendation"}
        yield {"spare_parts": self.spare.recommend(diag.get('diagnosis', ''))}
        yield {"status": "completed", "final": f"See diagnosis and recommendations"}
