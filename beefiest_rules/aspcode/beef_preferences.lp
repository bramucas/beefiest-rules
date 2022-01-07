#minimize { 1@3,I : outlier(I) }.
#minimize { OV@2,B1,B2,F : box(B1), box(B2), overlap(B1, B2, F, OV) }.
#minimize { IM@1,B : box(B), boximpurity(B, IM) }.