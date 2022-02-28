#const impurity = 0.
#const overlap = 0.
#const outliers = 0.

:- box(B), boximpurity(B, IM), IM >= impurity.
:- box(B1), box(B2), box_overlap(B1, B2), overlap(B1, B2, F, OV), OV >= overlap.
:- C=#count{ I : outlier(I) }, C >= outliers.