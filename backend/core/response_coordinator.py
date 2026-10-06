class AutonomousResponseCoordinator:
    def __init__(self):
        self.action_log = []

    def generate_response(self, root_cause_data: dict, health_score: float):
        asset_id = root_cause_data.get("failed_asset", "UNKNOWN")
        candidates = root_cause_data.get("root_cause_candidates", [])
        
        response_plan = {
            "incident_id": f"INC-{len(self.action_log) + 1}",
            "target_asset": asset_id,
            "actions": [],
            "self_healing_triggered": False
        }
        
        if health_score < 40.0:
            response_plan["actions"].append(f"CRITICAL: Dispatch Level 3 Engineering Team to {asset_id}")
            response_plan["actions"].append("Re-routing primary traffic to backup data center.")
            response_plan["self_healing_triggered"] = True
            
        elif candidates:
            culprit = candidates[0]['asset_id']
            response_plan["actions"].append(f"Isolating upstream dependency: {culprit}")
            response_plan["actions"].append(f"Restarting service on {culprit}")
            response_plan["self_healing_triggered"] = True
        else:
            response_plan["actions"].append("Monitor asset. Schedule preventive maintenance within 48 hours.")
            
        self.action_log.append(response_plan)
        return response_plan

response_coordinator = AutonomousResponseCoordinator()
