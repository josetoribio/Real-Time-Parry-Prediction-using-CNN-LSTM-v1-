A parry in Street Fighter III: 3rd Strike is a defensive mechanic that allows a player to negate an opponent's attack with zero blockstun by tapping toward the opponent.


A projectile is any attack that creates a moving hitbox separated from the character, such as Ryu's Hadoken.


 
Python
PyTorch
CNN + LSTM
OpenCV / PIL

V(1)
CNN extracts features per frame
LSTM learns motion over time
Output = parry vs no_parry

The model learned to distinguish early vs late frames rather than the precise timing window for parry execution. This revealed that folder-based labeling was insufficient for time-sensitive decision tasks.
