load('models/breast_subtype_classifier.rdata')
load("data/breast_validation_data.rdata")
met.pred <- predict(breast.model, newdata = met.scaled)
met.true.labels <- met.sample.anns$Pam50Subtype
idx <- met.true.labels %in% c("Basal","Her2","LumA","LumB")
met.true.labels[!idx] <- NA
met.true.labels[met.sample.anns$Pam50Subtype == "Basal"] <- "Basal-like"
met.true.labels[met.sample.anns$Pam50Subtype == "Her2"] <- "Her2 enriched"
met.true.labels[met.sample.anns$Pam50Subtype == "LumA"] <- "Luminal A"
met.true.labels[met.sample.anns$Pam50Subtype == "LumB"] <- "Luminal B"
lev <- c("Basal-like", "Her2 enriched", "Luminal A","Luminal B")
met.pred <- factor(met.pred,levels = lev)
met.true <- factor(met.true.labels ,levels = lev)

breast.cm <- confusionMatrix(met.pred,met.true)
print(breast.cm$byClass)

