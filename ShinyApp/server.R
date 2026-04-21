library(shiny)
library(class)

shinyServer(function(input, output) {

  train_data <- iris[, 1:4]
  train_labels <- iris$Species

  classification <- reactive({
    new_point <- data.frame(
      Sepal.Length = input$sepal_length,
      Sepal.Width  = input$sepal_width,
      Petal.Length  = input$petal_length,
      Petal.Width   = input$petal_width
    )

    distances <- sqrt(rowSums(sweep(train_data, 2, as.numeric(new_point))^2))
    k <- input$k
    nearest_idx <- order(distances)[1:k]
    nearest_labels <- train_labels[nearest_idx]

    vote_table <- table(nearest_labels)
    predicted <- names(which.max(vote_table))
    confidence <- max(vote_table) / k

    list(
      predicted  = predicted,
      confidence = confidence,
      neighbors  = iris[nearest_idx, ],
      distances  = distances[nearest_idx]
    )
  })

  output$predictionLabel <- renderText({
    res <- classification()
    paste0("Predicted Species: ", res$predicted)
  })

  output$confidenceLabel <- renderText({
    res <- classification()
    paste0("Confidence: ", round(res$confidence * 100), "%",
           " (", input$k, " neighbors)")
  })

  output$classPlot <- renderPlot({
    res <- classification()

    species_colors <- c(setosa = "#e74c3c", versicolor = "#3498db",
                        virginica = "#2ecc71")
    pt_col <- species_colors[as.character(iris$Species)]

    par(mar = c(5, 4, 3, 1), family = "sans")
    plot(iris$Petal.Length, iris$Petal.Width,
         col = pt_col, pch = 19, cex = 1.4,
         xlab = "Petal Length (cm)", ylab = "Petal Width (cm)",
         main = "Iris Petal Dimensions — Your Flower vs. Dataset")

    points(input$petal_length, input$petal_width,
           col = "#27ae60", pch = 18, cex = 5)

    pred_col <- species_colors[res$predicted]
    points(input$petal_length, input$petal_width,
           col = pred_col, pch = 18, cex = 3.5)

    legend("topleft",
           legend = c("setosa", "versicolor", "virginica", "Your Flower"),
           col = c(species_colors, "#27ae60"),
           pch = c(19, 19, 19, 18),
           pt.cex = c(1.4, 1.4, 1.4, 2.5),
           bg = "white")
  })

  output$neighborsTable <- renderTable({
    res <- classification()
    df <- res$neighbors
    df$Distance <- round(res$distances, 3)
    df
  }, striped = TRUE, hover = TRUE, bordered = TRUE)
})
