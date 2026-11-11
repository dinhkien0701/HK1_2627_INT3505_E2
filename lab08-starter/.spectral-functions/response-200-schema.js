module.exports = (targetVal, options, context) => {
  const content = targetVal && targetVal.content;

  if (options.requireContent === false) {
    return content
      ? [{ message: "204 responses must not declare content.", path: context.path }]
      : [];
  }

  const schema = content && content["application/json"] && content["application/json"].schema;
  return schema && Object.keys(schema).length > 0
    ? []
    : [{ message: "200 responses must declare a non-empty JSON schema.", path: context.path }];
};
