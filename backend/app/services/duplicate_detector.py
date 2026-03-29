from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict
from difflib import SequenceMatcher

class DuplicateDetector:
    """Advanced duplicate detection with fuzzy matching"""
    
    @staticmethod
    def similarity_ratio(a: str, b: str) -> float:
        """Calculate string similarity 0-1"""
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    @staticmethod
    def is_duplicate(
        new_transaction: dict,
        existing: List[Dict],
        time_window_minutes: int = 30,
        similarity_threshold: float = 0.75,
        amount_variance: float = 0.05  # 5% variance allowed
    ) -> Tuple[bool, Optional[Dict]]:
        """
        Smart duplicate detection considering:
        - Time proximity (within X minutes)
        - Description similarity (fuzzy matching)
        - Amount variance (within ±5%)
        - Transaction type consistency
        """
        
        new_time = new_transaction.get('timestamp') or datetime.utcnow()
        if isinstance(new_time, str):
            new_time = datetime.fromisoformat(new_time.replace('Z', '+00:00'))
            
        new_amount = abs(new_transaction['amount'])
        new_desc = new_transaction['description']
        new_type = new_transaction['transaction_type']
        
        for existing_txn in existing:
            # 1. Check time window
            exist_time = existing_txn.get('timestamp')
            if isinstance(exist_time, str):
                exist_time = datetime.fromisoformat(exist_time.replace('Z', '+00:00'))
                
            time_diff = abs((new_time - exist_time).total_seconds()) / 60.0
            if time_diff > time_window_minutes:
                continue
            
            # 2. Check amount variance
            existing_amount = abs(existing_txn['amount'])
            if existing_amount == 0 and new_amount == 0:
                pass # Both 0 is match
            elif existing_amount == 0:
                continue
            else:
                variance = abs(new_amount - existing_amount) / existing_amount
                if variance > amount_variance:
                    continue
            
            # 3. Check description similarity
            desc_similarity = DuplicateDetector.similarity_ratio(
                new_desc, 
                existing_txn['description']
            )
            if desc_similarity < similarity_threshold:
                continue
            
            # 4. Check transaction type
            if new_type != existing_txn['transaction_type']:
                continue
            
            # All checks passed - it's a duplicate!
            return True, existing_txn
        
        return False, None
    
    @staticmethod
    def find_duplicate_clusters(transactions: List[Dict]) -> List[List[Dict]]:
        """Find groups of potential duplicates for batch operations"""
        clusters = []
        processed = set()
        
        for i, txn in enumerate(transactions):
            if i in processed:
                continue
            
            cluster = [txn]
            processed.add(i)
            
            for j, other_txn in enumerate(transactions[i+1:], start=i+1):
                if j in processed:
                    continue
                
                is_dup, _ = DuplicateDetector.is_duplicate(
                    txn, [other_txn], 
                    time_window_minutes=60
                )
                
                if is_dup:
                    cluster.append(other_txn)
                    processed.add(j)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
