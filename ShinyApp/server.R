library(shiny)

shinyServer(function(input, output) {

  model <- lm(mpg ~ wt + hp + factor(cyl) + am, data = mtcars)

  predictedMPG <- reactive({
    newdata <- data.frame(
      wt  = input$wt,
      hp  = input$hp,
      cyl = as.numeric(input$cyl),
      am  = as.numeric(input$am)
    )
    predict(model, newdata)
  })

  output$predictionLabel <- renderText({
    paste0("Predicted MPG: ", round(predictedMPG(), 1))
  })

  output$mpgPlot <- renderPlot({
    pred <- predictedMPG()
    par(mar = c(5, 4, 3, 1))

    palette <- ifelse(mtcars$am == 1, "#2980b9", "#e74c3c")
    pch_vec <- c(16, 17, 15)[match(mtcars$cyl, c(4, 6, 8))]

    plot(mtcars$wt, mtcars$mpg,
         xlab = "Weight (1000 lbs)", ylab = "Miles Per Gallon",
         main = "Your Prediction vs. Real Cars (mtcars)",
         col = palette, pch = pch_vec, cex = 1.6,
         xlim = c(1.2, 5.8), ylim = c(8, 38))

    points(input$wt, pred, col = "#27ae60", pch = 18, cex = 4)

    legend("topright",
           legend = c("Manual", "Automatic", "4 cyl", "6 cyl", "8 cyl", "Your Car"),
           col    = c("#2980b9", "#e74c3c", "grey40", "grey40", "grey40", "#27ae60"),
           pch    = c(16, 16, 16, 17, 15, 18),
           pt.cex = c(1.4, 1.4, 1.4, 1.4, 1.4, 2.2),
           bg = "white")
  })

  output$modelSummary <- renderPrint({
    summary(model)
  })
})
