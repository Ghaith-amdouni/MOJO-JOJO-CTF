# Bodreya Drift: Municipal Chaos

**Category**: Misc / Programming
**Difficulty**: Hard (Strict Timeout)

## Description
Welcome to **Bodreya**, the only city where the roads are topologically impossible and the traffic lights are merely suggestions. The Municipality has hired *you* (budget cuts, sorry) to optimize the delivery route for the Mayor's "Mojo Jojo Special Sauce".

## Connect
`nc <HOST> <PORT>`

## Distribution
*   **Provide to players**: `public_server.py` (This allows them to understand the Hilbert Curve logic without seeing the real flag).
*   **Do NOT provide**: `solve.py` (That's for you).
*   **Do NOT provide**: `server.py` (Contains the real flag).

## Notes
The server timeout is strict. Python default `sorted()` might be too slow if you don't calculate the Hilbert distances efficiently. Batch processing is key.
