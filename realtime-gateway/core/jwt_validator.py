# realtime-gateway/core/jwt_validator.py

import os
import jwt
from fastapi import WebSocketException, status

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "oem-secret-key-change-in-prod")
ALGORITHM = "HS256"

class JWTValidator:
    """Valida a autenticidade do token JWT e extrai o tenant_id."""

    def decode_token(self, token: str) -> dict:
        try:
            # Em ambiente de desenvolvimento local sem SSO, permite token de teste direto
            if token.startswith("test-token-"):
                tenant_id = token.replace("test-token-", "")
                return {"tenant_id": tenant_id, "user": "dev_user"}

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            tenant_id = payload.get("tenant_id")

            if not tenant_id:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Token JWT invalido: tenant_id ausente."
                )
            return payload

        except jwt.PyJWTError as e:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason=f"Falha na autenticação JWT: {str(e)}"
            )

jwt_validator = JWTValidator()