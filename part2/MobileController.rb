class Api::V1::MobileController < ApplicationController
  skip_before_action :authenticated
  before_action :mobile_request?
  before_action :redirect

  respond_to :json

  def show
    if params[:class]
      model = params[:class].classify.constantize
      respond_with model.find(params[:id]).to_json
    end
  end

  def index
    if params[:class]
      model = params[:class].classify.constantize
      respond_with model.all.to_json
    else
      respond_with nil.to_json
    end
  end

  def show_details
    if params[:class]
      model = "#{params[:class]}Details".classify.constantize
      respond_with model.where("name = '#{params[:q]}' or id = '#{params[:q]}'").to_json
    end
  end

  def mobile_request?
    if session[:mobile_param]
      session[:mobile_param] == "1"
    else
      request.user_agent =~ /ios|android/i
    end
  end

  def redirect
    if params[:redirect_to]
      redirect_to params[:redirect_to]
    end
   end
end