library(shiny)

shinyUI(fluidPage(
  titlePanel("MPG Predictor — Estimate Your Car's Fuel Efficiency"),

  sidebarLayout(
    sidebarPanel(
      h4("Car Specifications"),
      sliderInput("wt", "Weight (1000 lbs):", min = 1.5, max = 5.5,
                  value = 3.2, step = 0.1),
      sliderInput("hp", "Horsepower:", min = 50, max = 350,
                  value = 150, step = 5),
      radioButtons("cyl", "Number of Cylinders:",
                   choices = c("4" = 4, "6" = 6, "8" = 8), selected = 6),
      selectInput("am", "Transmission:",
                  choices = c("Automatic" = 0, "Manual" = 1), selected = 0),
      checkboxInput("showModel", "Show model details", value = FALSE),
      hr(),
      h4("Documentation"),
      p("This app predicts a car's miles-per-gallon (MPG) based on four
         characteristics you select above:"),
      tags$ul(
        tags$li(strong("Weight"), "— vehicle weight in thousands of pounds."),
        tags$li(strong("Horsepower"), "— engine horsepower."),
        tags$li(strong("Cylinders"), "— number of engine cylinders (4, 6, or 8)."),
        tags$li(strong("Transmission"), "— automatic or manual.")
      ),
      p("Adjust the sliders and buttons, and the predicted MPG updates instantly
         on the right panel. The scatter plot shows how your prediction compares
         to real cars in the", code("mtcars"), "dataset."),
      p("Check", em("Show model details"), "to see the regression coefficients.")
    ),

    mainPanel(
      h3(textOutput("predictionLabel")),
      br(),
      plotOutput("mpgPlot"),
      br(),
      conditionalPanel(
        condition = "input.showModel == true",
        h4("Linear Model Summary"),
        verbatimTextOutput("modelSummary")
      )
    )
  )
))
