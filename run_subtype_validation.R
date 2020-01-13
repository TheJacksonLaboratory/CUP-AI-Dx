library(randomForest)
library(caret)

args = commandArgs(trailingOnly=TRUE)
if (length(args)>1){
  out_dir <- args[2]
}else{
  out_dir <- 'output'
}
dir.create(out_dir)
print(args)

if(args[1]=='breast_cancer'){
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
  write.csv(breast.cm$byClass, file=paste0(out_dir,'/breast_subtype_result'))
  
  
}else if(args[1]=='ovarian_cancer'){
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
  write.csv(ovarian.cm$byClass, file=paste0(out_dir,'/ovarian_subtype_result'))
}


