#minimize { 1@4,I : outlier(I) }.
#minimize { OV@3,B1,B2,F : box(B1), box(B2), box_overlap(B1, B2), overlap(B1, B2, F, OV) }.
#minimize { IM@2,B : box(B), boximpurity(B, IM) }.

#minimize { W@1,B,F : boxfeature_width(B, F, W) }.