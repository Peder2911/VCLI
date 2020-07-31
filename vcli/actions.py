
import views

class Actions:
    def estimate(self,
            dataset,
            name, 
            spec,
            periodization,
            steps=[1],
            estimator = "sklearn.ensemble.RandomForestClassifier",
            est_args={},
            outcome_type="prob"):
        """
        Train a new model
        """

        df = views.DATASETS[dataset].df
        spec = views.specs.models.cm[spec]
        periods = views.specs.periods.get_periods_by_name(periodization)

        m = views.Model(
                name = name,
                estimator = eval(estimator)(**est_args),
                steps = steps,
                periods=[*periods.values()],
                outcome_type = outcome_type,
                col_outcome = spec["col_outcome"],
                cols_features = spec["cols_features"]
            )

        m.fit_estimators(df)
        predictions = m.predict(df)
        df_merged = views.utils.data.assign_into_df(df,predictions)
        m.evaluate(df_merged)
        print(m.scores)
