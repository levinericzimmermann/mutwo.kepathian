local plain = SILE.require('classes.plain')
plain:loadPackage("simpletable", {
      tableTag = "table",
      trTag = "tr",
      tdTag = "td"
})
plain:registerCommand("kepathian", function (options, content)
    SILE.call("table", options, content)
end)
