from ...build.Builder import BuildApplication

# Area to test entire application
ApplicationWorkbench: BuildApplication = BuildApplication(conf_file="./src/build/conf/build.json")

ApplicationWorkbench.build()
