#const maxboxes = 3.
number(1..maxboxes).

%% Pick a number of boxes
1{ boxes(B) : number(B) }1.
box(1..B) :- boxes(B).

%% Blindly select the features used for each box
2 { boxfeature(B,F) : feature(F), target(T), F != T } :- box(B).

%% Map points in relation to each other so we know for each point and feature if they are to the left
%% to the right or in the same position as another given instance. This helps us avoid further arithmetic calculations
left(I1, I2, F) :- instance(I1), instance(I2), feature(F), target(T), value(I1, F, V1), value(I2, F, V2), V1 <= V2, F != T.
right(I1, I2, F) :- instance(I1), instance(I2), feature(F), target(T), value(I1, F, V1), value(I2, F, V2), V1 >= V2, F != T.

2 { boxlimit(B, F, I, V) : value(I,F,V) } 2 :- boxfeature(B,F).
boxlimit(B, F, V) :- boxlimit(B, F, _, V).

boxfeature_inlier(B, F, I) :- boxlimit(B, F, L1, _), boxlimit(B, F, L2, _), left(L1, L2, F), L1 != L2,
                                    instance(I), right(I, L1, F), left(I, L2, F).
boxfeature_outlier(B, F, I) :- instance(I), boxfeature(B,F), not boxfeature_inlier(B, F, I).

box_outlier(B, I) :- boxfeature_outlier(B, _, I).
box_inlier(B, I) :- box(B), instance(I), not box_outlier(B,I).

outlier(I) :- instance(I), not box_inlier(_, I).

%% Count targets in each box
boxinliercount(B, IC) :- IC=#count{ I : box_inlier(B, I)}, box(B).
boxpositives(B, P) :- box(B), P=#count{ I : box_inlier(B, I), value(I, T, 1) }, P > 0.
boxnegatives(B, N) :- box(B), N=#count{ I : box_inlier(B, I), value(I, T, 0) }, N > 0.

boxmain(B, 1) :- boxpositives(B, P), boxnegatives(B, N), P > N.
boxmain(B, 0) :- boxpositives(B, P), boxnegatives(B, N), P < N.

boximpurity(B, N) :- boxmain(B, 1), boxnegatives(B, N).
boximpurity(B, P) :- boxmain(B, 0), boxnegatives(B, P).

% Feature is shared but limits don't overlap (L1 R1) [L2 R2] = 0
overlap(B1, B2, F, 0) :- box(B1), box(B2), boxfeature(B1, F), boxfeature(B2, F), B1 < B2, boxlimit(B1, F, L1, LV1), boxlimit(B1, F, R1, RV1), L1 != R1,
                            boxlimit(B2, F, L2, LV2), boxlimit(B2, F, R2, RV2), L2 != R2, left(L1, R1, F), left(R1, L2, F), left(L2, R2, F).

% Feature is shared and limits overlap (L1 [L2 R1) R2] = R1 - L2
overlap(B1, B2, F, OV) :- box(B1), box(B2), boxfeature(B1, F), boxfeature(B2, F), B1 < B2, boxlimit(B1, F, L1, LV1), boxlimit(B1, F, R1, RV1), L1 != R1,
                            boxlimit(B2, F, L2, LV2), boxlimit(B2, F, R2, RV2), L2 != R2, left(L1, R1, F), left(L2, R1, F), left(L2, R2, F), OV = RV1 - LV2.

% Feature is not shared. L1 R1 = R1 - L1
overlap(B1, B2, F, OV) :- box(B1), box(B2), boxfeature(B1, F), not boxfeature(B2, F), B1 != B2, boxlimit(B1, F, L1, LV1), boxlimit(B1, F, R1, RV1), L1 != R1,
                            left(L1, R1, F), OV = RV1 - LV1.

:- box(B), not boxmain(B, _).

#show box/1.
#show boxfeature/2.

#show boxlimit/3.

#show boxmain/2.
#show boximpurity/2.

#show outlier/1.
