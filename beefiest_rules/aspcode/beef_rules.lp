#const boxes = 3.
box(1..boxes).

feature_value(F,V) :- value(_, F, V), feature(F), target(T), F != T.

%% Map points in relation to each other so we know for each point. This helps us avoid further arithmetic calculations
left(F, V1, V2) :- feature(F), feature_value(F, V1), feature_value(F, V2), V1 <= V2.

{ boxlimits(B, F, V1, V2) : left(F, V1, V2) } 1 :- box(B), feature(F), target(T), F != T.
boxfeature(B, F) :- boxlimits(B, F, _, _).

boxfeature_width(B, F, W) :- boxlimits(B, F, V1, V2), W = V2 - V1.

boxfeature_inlier(B, F, I, V) :- boxlimits(B, F, L1, L2), value(I, F, V), left(F, V, L2), left(F, L1, V).
boxfeature_inlier(B, F, I) :- boxfeature_inlier(B, F, I, _).
boxfeature_outlier(B, F, I) :- instance(I), boxfeature(B,F), not boxfeature_inlier(B, F, I).

box_outlier(B, I) :- boxfeature_outlier(B, _, I).
box_inlier(B, I) :- box(B), instance(I), not box_outlier(B,I).

outlier(I) :- instance(I), not box_inlier(_, I).

% Since we don't need the Impurity metric, we just tag pairs of inliers that differ in value for the target
% Then we just minimize the cardinality of those predicates to homogenize the contents of each box.
impurepair(B, I1, I2) :- box_inlier(B, I1), box_inlier(B, I2), I1 > I2, target(T), value(I1, T, V1), value(I2, T, V2), V1 != V2.

% Feature is shared but limits don't overlap (L1 R1) [L2 R2] = 0
overlap(B1, B2, F, 0) :- box(B1), box(B2), boxfeature(B1, F), boxfeature(B2, F), B1 < B2, boxlimits(B1, F, L1, R1),
                            boxlimits(B2, F, L2, R2), left(F, R1, L2).

% Feature is shared and limits overlap (L1 [L2 R1) R2] = R1 - L2
overlap(B1, B2, F, OV) :- box(B1), box(B2), boxfeature(B1, F), boxfeature(B2, F), B1 < B2, boxlimits(B1, F, L1, R1),
                            boxlimits(B2, F, L2, R2), left(F, L2, R1), OV = R1 - L2.

% Feature is not shared. L1 R1 = R1 - L1
overlap(B1, B2, F, OV) :- box(B1), box(B2), boxfeature(B1, F), not boxfeature(B2, F), B1 != B2, boxlimits(B1, F, L1, R1),
                            OV = R1 - L1.

no_overlap(B1, B2) :- overlap(B1, B2, F, 0), feature(F).
box_overlap(B1, B2) :- box(B1), box(B2), not no_overlap(B1, B2), B1 < B2.

:- box(B), not box_inlier(B, _).
:- box(B), not boxlimits(B, _, _, _).

#show box/1.
#show boxfeature/2.
#show boxlimits/4.