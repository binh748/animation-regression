import numpy as np
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def create_genre_encodings(df, unique_genres):
    for genre in unique_genres:
        df['is_' + genre] = df.apply(
            lambda x: genre in x['genres'], axis=1).astype(int)


def feature_target_selection(features, target, df):
    X = df.loc[:, features]
    y = df[target]
    return X, y


def initial_split(X, y):
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.2, random_state=4444)
    return X_train_val, X_test, y_train_val, y_test


def split_and_simple_validate(X_train_val, y_train_val):
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=.25, random_state=4444)

    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)

    train_score = lr_model.score(X_train, y_train)
    val_score = lr_model.score(X_val, y_val)

    print(f'{"Training R^2:": <30}', round(train_score, 3))
    print(f'{"Validation R^2:": <30}', round(val_score, 3))
    print(f'{"Intercept:": <30} {lr_model.intercept_[0]}')
    print('\nFeature coefficients: \n')

    # For some reason, coef are in list of lists
    for feature, coef in zip(X_train_val.columns, lr_model.coef_[0]):
        print(f'{feature: <30} {coef:.2f}')

#     return X_train, X_val, y_train, y_val, lr_model


def cv(X_train_val, y_train_val, cv_records):
    lr_model = LinearRegression()
    kf = KFold(n_splits=5, shuffle=True, random_state=4444)

    scores = cross_validate(lr_model, X_train_val, y_train_val,
                            cv=kf, scoring='r2', return_train_score=True)
    mean_train_score = round(np.mean(scores['train_score']), 3)
    mean_val_score = round(np.mean(scores['test_score']), 3)

    print(scores['train_score'])
    print(f'{"Mean train R^2:": <20}', mean_train_score, '\n')

    print(scores['test_score'])
    print(f'{"Mean val R^2:": <20}', mean_val_score)

    cv_records.append(record_cv(mean_train_score, mean_val_score))


def record_cv(mean_train_score, mean_val_score):
    cv_dict = {}
    model = input("Model: ")
    label = input("Iteration description: ")
    cv_dict['model'] = model
    cv_dict['label'] = label
    cv_dict['mean_train_score'] = mean_train_score
    cv_dict['mean_val_score'] = mean_val_score
    return cv_dict


def final_train_and_test(X_train_val, y_train_val, X_test, y_test):
    lr_model = LinearRegression()
    lr_model.fit(X_train_val, y_train_val)

    train_score = lr_model.score(X_train_val, y_train_val)
    test_score = lr_model.score(X_test, y_test)
    train_mae = mean_absolute_error(y_train_val, lr_model.predict(X_train_val))
    test_mae = mean_absolute_error(y_test, lr_model.predict(X_test))

    print(f'{"Training R^2:": <30}', round(train_score, 3))
    print(f'{"Test R^2:": <30}', round(test_score, 3), '\n')

    print(f'{"Training MAE:": <30}', round(train_mae, 3))
    print(f'{"Test MAE:": <30}', round(test_mae, 3), '\n')

    print(f'{"Intercept:": <30} {lr_model.intercept_[0]}')
    print('\nFeature coefficients: \n')

    for feature, coef in zip(X_train_val.columns, lr_model.coef_[0]):
        print(f'{feature: <30} {coef:.2f}')

    return lr_model
