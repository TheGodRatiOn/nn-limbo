import numpy as np

import logs


def softmax(predictions):
    '''
    Computes probabilities from scores

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output

    Returns:
      probs, np array of the same shape as predictions - 
        probability for every class, 0..1
    '''
    logs.m('softmax')
    logs.pr('predictions', predictions)
    logs.pr('predictions.ndim', predictions.ndim)
    
    if predictions.ndim == 1:
        probs = predictions - np.max(predictions)
        logs.pr('predictions - np.max(predictions)', probs)
        
        probs = np.exp(probs)
        logs.pr('np.exp(probs)', probs)
        
        probs /= probs.sum()
        logs.pr('probs / probs.sum()', probs)

        assert np.isclose(probs.sum(), 1)
    else:
        batch_size = predictions.shape[0]

        logs.pr('np.max(predictions, axis=1).reshape(batch_size, 1)', np.max(predictions, axis=1).reshape(batch_size, 1))
        probs = predictions - np.max(predictions, axis=1).reshape(batch_size, 1)
        logs.pr('predictions - np.max(predictions, axis=1).reshape(batch_size, 1)', probs)
        
        probs = np.exp(probs)
        logs.pr('np.exp(probs)', probs)
        
        logs.pr('probs.sum(axis=1).reshape(batch_size, 1)', probs.sum(axis=1).reshape(batch_size, 1))
        probs /= probs.sum(axis=1).reshape(batch_size, 1)
        logs.pr('probs / probs.sum(axis=1).reshape(batch_size, 1)', probs)

        assert np.all(np.isclose(probs.sum(axis=1), 1))
    
    logs.me('softmax')
    
    return probs


def cross_entropy_loss(probs, target_index):
    '''
    Computes cross-entropy loss

    Arguments:
      probs, np array, shape is either (N) or (batch_size, N) -
        probabilities for every class
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss: single value
    '''
    logs.m('cross_entropy_loss')
    logs.pr('probs', probs)
    logs.pr('probs.ndim', probs.ndim)
    logs.pr('target_index', target_index)
    
    if probs.ndim == 1:
        logs.pr('probs[target_index]', probs[target_index])
        logs.pr('np.log(probs[target_index])', np.log(probs[target_index]))
        logs.pr('-np.log(probs[target_index])', -np.log(probs[target_index]))
        
        loss = -np.log(probs[target_index])
    else:
        batch_size = probs.shape[0]
        target_index = (np.arange(batch_size), target_index.reshape(batch_size))
        
        logs.pr('target_index', target_index)
        logs.pr('probs[target_index]', probs[target_index])
        logs.pr('np.log(probs[target_index])', np.log(probs[target_index]))
        logs.pr('-np.log(probs[target_index])', -np.log(probs[target_index]))
        logs.pr('np.mean(-np.log(probs[target_index]))', np.mean(-np.log(probs[target_index])))
        
        loss = np.mean(-np.log(probs[target_index]))
    
    logs.me('cross_entropy_loss')
    
    return loss


def softmax_with_cross_entropy(predictions, target_index):
    '''
    Computes softmax and cross-entropy loss for model predictions,
    including the gradient

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss, single value - cross-entropy loss
      dprediction, np array same shape as predictions - gradient of predictions by loss value
    '''
    logs.m('softmax_with_cross_entropy')
    logs.pr('predictions', predictions)
    logs.pr('predictions.ndim', predictions.ndim)
    logs.pr('target_index', target_index)
    
    probs = softmax(predictions)
    loss = cross_entropy_loss(probs, target_index)
    dprediction = probs.copy()
    
    if predictions.ndim == 1:
        dprediction[target_index] -= 1
    else:
        batch_size = predictions.shape[0]
        ti = (np.arange(batch_size), target_index.reshape(batch_size))
        
        logs.pr('ti', ti)
        
        dprediction[ti] -= 1
    
    logs.pr('loss', loss)
    logs.pr('dprediction', dprediction)
    logs.me('softmax_with_cross_entropy')

    return loss, dprediction


def l2_regularization(W, reg_strength):
    '''
    Computes L2 regularization loss on weights and its gradient

    Arguments:
      W, np array - weights
      reg_strength - float value

    Returns:
      loss, single value - l2 regularization loss
      gradient, np.array same shape as W - gradient of weight by l2 loss
    '''

    # TODO: implement l2 regularization and gradient
    # Your final implementation shouldn't have any loops
    raise Exception("Not implemented!")

    return loss, grad
    

def linear_softmax(X, W, target_index):
    '''
    Performs linear classification and returns loss and gradient over W

    Arguments:
      X, np array, shape (num_batch, num_features) - batch of images
      W, np array, shape (num_features, classes) - weights
      target_index, np array, shape (num_batch) - index of target classes

    Returns:
      loss, single value - cross-entropy loss
      gradient, np.array same shape as W - gradient of weight by loss

    '''
    predictions = np.dot(X, W)

    # TODO implement prediction and gradient over W
    # Your final implementation shouldn't have any loops
    raise Exception("Not implemented!")
    
    return loss, dW


class LinearSoftmaxClassifier():
    def __init__(self):
        self.W = None

    def fit(self, X, y, batch_size=100, learning_rate=1e-7, reg=1e-5,
            epochs=1):
        '''
        Trains linear classifier
        
        Arguments:
          X, np array (num_samples, num_features) - training data
          y, np array of int (num_samples) - labels
          batch_size, int - batch size to use
          learning_rate, float - learning rate for gradient descent
          reg, float - L2 regularization strength
          epochs, int - number of epochs
        '''

        num_train = X.shape[0]
        num_features = X.shape[1]
        num_classes = np.max(y)+1
        if self.W is None:
            self.W = 0.001 * np.random.randn(num_features, num_classes)

        loss_history = []
        for epoch in range(epochs):
            shuffled_indices = np.arange(num_train)
            np.random.shuffle(shuffled_indices)
            sections = np.arange(batch_size, num_train, batch_size)
            batches_indices = np.array_split(shuffled_indices, sections)

            # TODO implement generating batches from indices
            # Compute loss and gradients
            # Apply gradient to weights using learning rate
            # Don't forget to add both cross-entropy loss
            # and regularization!
            raise Exception("Not implemented!")

            # end
            print("Epoch %i, loss: %f" % (epoch, loss))

        return loss_history

    def predict(self, X):
        '''
        Produces classifier predictions on the set
       
        Arguments:
          X, np array (test_samples, num_features)

        Returns:
          y_pred, np.array of int (test_samples)
        '''
        y_pred = np.zeros(X.shape[0], dtype=np.int)

        # TODO Implement class prediction
        # Your final implementation shouldn't have any loops
        raise Exception("Not implemented!")

        return y_pred
