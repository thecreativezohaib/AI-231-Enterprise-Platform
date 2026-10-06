from backend.core.database import neo4j_driver
import networkx as nx

class RootCauseEngine:
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def identify_root_cause(self, failed_asset_id: str):
        if not self.driver:
            return {"error": "Neo4j not connected"}
        
        # Traverse graph to find upstream dependencies that might be failing
        query = """
        MATCH (a:Asset {asset_id: $asset_id})-[:DEPENDS_ON*1..3]->(upstream:Asset)
        RETURN upstream.asset_id as uid, upstream.type as utype
        """
        
        with self.driver.session() as session:
            result = session.run(query, asset_id=failed_asset_id)
            dependencies = [{"asset_id": record["uid"], "type": record["utype"]} for record in result]
            
        if dependencies:
            return {
                "failed_asset": failed_asset_id,
                "root_cause_candidates": dependencies,
                "recommendation": f"Check upstream {dependencies[0]['type']} ({dependencies[0]['asset_id']})"
            }
        return {
            "failed_asset": failed_asset_id,
            "root_cause_candidates": [],
            "recommendation": "Isolated failure. Dispatch maintenance team to asset."
        }

rca_engine = RootCauseEngine(neo4j_driver)
