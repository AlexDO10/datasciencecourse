library(shiny)

shinyUI(
  navbarPage(
    "Iris Flower Classifier",

    tabPanel(
      "How to Use This App",
      fluidRow(
        column(8, offset = 2,
          h2("Welcome to the Iris Flower Classifier"),
          p("This application uses a", strong("k-Nearest Neighbors (kNN)"),
            "algorithm to predict the species of an iris flower based on four
             physical measurements you provide."),
          h3("Getting Started"),
          tags$ol(
            tags$li("Click the", strong("Classifier"), "tab above."),
            tags$li("Use the", strong("sliders"), "to set the flower's sepal
                     length, sepal width, petal length, and petal width (all in
                     centimeters)."),
            tags$li("Choose the", strong("number of neighbors (k)"),
                     "for the kNN algorithm using the slider."),
            tags$li("The predicted species appears instantly in the main panel,
                     along with a confidence score and a scatter plot showing
                     your flower among the real Iris dataset.")
          ),
          h3("What Do the Outputs Mean?"),
          tags$ul(
            tags$li(strong("Predicted Species:"),
                    "The species the model thinks your flower belongs to —",
                    em("setosa, versicolor,"), "or", em("virginica.")),
            tags$li(strong("Confidence:"),
                    "The proportion of the k nearest neighbors that voted for
                     the predicted species. Higher is better."),
            tags$li(strong("Scatter Plot:"),
                    "Shows petal length vs. petal width for all 150 iris flowers.
                     Your flower is the large green diamond. The background colors
                     indicate the model's decision regions."),
            tags$li(strong("Nearest Neighbors Table:"),
                    "The actual data rows of the k neighbors closest to your
                     flower, so you can see which real flowers it resembles.")
          ),
          h3("About the Dataset"),
          p("The", code("iris"), "dataset (built into R) contains 150
             observations of three iris species, with 50 flowers each. It was
             introduced by statistician Ronald Fisher in 1936 and is one of the
             most well-known datasets in pattern recognition."),
          h3("Source Code"),
          p("The full source code (ui.R and server.R) is available on",
            a("GitHub.", href = "https://github.com/AlexDO10/datasciencecourse",
              target = "_blank"))
        )
      )
    ),

    tabPanel(
      "Classifier",
      sidebarLayout(
        sidebarPanel(
          h4("Flower Measurements (cm)"),
          sliderInput("sepal_length", "Sepal Length:",
                      min = 4.0, max = 8.0, value = 5.8, step = 0.1),
          sliderInput("sepal_width", "Sepal Width:",
                      min = 2.0, max = 4.5, value = 3.0, step = 0.1),
          sliderInput("petal_length", "Petal Length:",
                      min = 1.0, max = 7.0, value = 4.0, step = 0.1),
          sliderInput("petal_width", "Petal Width:",
                      min = 0.1, max = 2.5, value = 1.2, step = 0.1),
          hr(),
          h4("Model Setting"),
          sliderInput("k", "Number of Neighbors (k):",
                      min = 1, max = 15, value = 5, step = 2),
          helpText("A higher k makes the model smoother but less sensitive.")
        ),

        mainPanel(
          h3(textOutput("predictionLabel")),
          h4(textOutput("confidenceLabel")),
          br(),
          plotOutput("classPlot", height = "420px"),
          br(),
          h4("Nearest Neighbors"),
          tableOutput("neighborsTable")
        )
      )
    )
  )
)
