load('models/ovarian_subtype_classifier.rdata')
load("data/ovarian_validation_data.rdata")
library(hgu133plus2.db)
aocs.pred <- predict(ovarian.model, newdata = aocs.scaled)
aocs.true.labels <- aocs.sample.anns$MolSubtype
idx <- aocs.true.labels %in% c(1,2,4,5)
aocs.true.labels[!idx] <- NA
aocs.true.labels[aocs.sample.anns$MolSubtype == 1] <- "Mesenchymal"
aocs.true.labels[aocs.sample.anns$MolSubtype == 2] <- "Immunoreactive"
aocs.true.labels[aocs.sample.anns$MolSubtype == 4] <- "Differentiated"
aocs.true.labels[aocs.sample.anns$MolSubtype == 5] <- "Proliferative"

lev <- c("Mesenchymal", "Immunoreactive", "Differentiated","Proliferative")
aocs.pred <- factor(aocs.pred,levels = lev)
aocs.true <- factor(aocs.true.labels ,levels = lev)

ovarian.cm <- confusionMatrix(aocs.pred,aocs.true)
print(ovarian.cm$byClass)
